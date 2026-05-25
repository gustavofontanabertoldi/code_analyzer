import re

import javalang


def _find_matching(text, start, open_char, close_char):
    depth = 0
    in_string = False
    escaped = False

    for index in range(start, len(text)):
        char = text[index]

        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == in_string:
                in_string = False
            continue

        if char in ('"', "'"):
            in_string = char
        elif char == open_char:
            depth += 1
        elif char == close_char:
            depth -= 1
            if depth == 0:
                return index

    return -1


def _split_record_components(components):
    parts = []
    start = 0
    depth = {"(": 0, "<": 0, "[": 0}

    for index, char in enumerate(components):
        if char == "(":
            depth["("] += 1
        elif char == ")":
            depth["("] -= 1
        elif char == "<":
            depth["<"] += 1
        elif char == ">":
            depth["<"] -= 1
        elif char == "[":
            depth["["] += 1
        elif char == "]":
            depth["["] -= 1
        elif char == "," and all(value == 0 for value in depth.values()):
            parts.append(components[start:index].strip())
            start = index + 1

    last = components[start:].strip()
    if last:
        parts.append(last)

    return parts


def _component_to_field(component):
    without_annotations = re.sub(r"@\w+(?:\.\w+)*(?:\([^()]*\))?\s*", "", component)
    tokens = without_annotations.strip().split()

    if len(tokens) < 2:
        return None

    name = tokens[-1].replace("...", "[]")
    field_type = " ".join(tokens[:-1]).replace("...", "[]")
    return f"    private {field_type} {name};"


def _normalize_records(data):
    pattern = re.compile(r"((?:public|protected|private|abstract|static|final)\s+)*record\s+(\w+)\s*\(")
    output = []
    position = 0

    while True:
        match = pattern.search(data, position)
        if not match:
            output.append(data[position:])
            break

        params_start = match.end() - 1
        params_end = _find_matching(data, params_start, "(", ")")
        if params_end == -1:
            output.append(data[position:])
            break

        body_start = data.find("{", params_end)
        if body_start == -1:
            output.append(data[position:])
            break

        body_end = _find_matching(data, body_start, "{", "}")
        if body_end == -1:
            output.append(data[position:])
            break

        output.append(data[position:match.start()])

        modifiers = (match.group(1) or "").strip()
        class_name = match.group(2)
        components = data[params_start + 1:params_end]
        body = data[body_start + 1:body_end]
        fields = [
            field
            for field in (_component_to_field(component) for component in _split_record_components(components))
            if field
        ]

        class_header = f"{modifiers} class {class_name}".strip()
        class_body = "\n".join(fields)
        if body.strip():
            class_body = f"{class_body}\n{body}" if class_body else body

        output.append(f"{class_header} {{\n{class_body}\n}}")
        position = body_end + 1

    return "".join(output)

def parse_java_file(path):

    with open(path, "r", encoding="utf-8") as file:
        data = file.read()

    try:
        tree = javalang.parse.parse(data)
    except javalang.parser.JavaSyntaxError:
        if " record " not in data and "\nrecord " not in data:
            raise
        tree = javalang.parse.parse(_normalize_records(data))

    return tree
