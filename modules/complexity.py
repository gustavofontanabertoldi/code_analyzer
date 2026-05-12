import javalang

def analyze_complexity(path):
    count = 1

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = file.read()

        tree = javalang.parse.parse(data)

        for p, node in tree:
            if isinstance(node, javalang.tree.IfStatement):
                    count += 1
            
        return count
    except:
         return -1