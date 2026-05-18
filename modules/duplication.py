def analyze_duplication(java_files):

    duplications = 0
    blocks = {}

    for java_file in java_files:
        with open(java_file, "r", encoding="utf-8") as f:
            lines = [
                lines.strip()
                for line in f.readlines()
                if line.strip()
            ]

        for i in range(len(lines) - 4):
            block = "".join(lines[i:i+5]).strip()
            if not block:
                continue
            if block in blocks:
                duplications += 1
            else:
                blocks[block] = java_file

    return duplications