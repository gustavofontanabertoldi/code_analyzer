import javalang

def analyze_complexity(path):
    count = 1

    with open("path", "r", encoding="utf-8") as f:
        data = f.read()

    tree = javalang.parse.parse(data)

    for path, node in tree:
        if isinstance(node, javalang.tree.IfStatement):
            count += 1
    
    return count