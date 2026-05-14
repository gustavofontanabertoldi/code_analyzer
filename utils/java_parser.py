import javalang

def parse_java_file(path):

    with open(path, "r", encoding="utf-8") as file:
        data = file.read()
    
    tree = javalang.parse.parse(data)
    return tree