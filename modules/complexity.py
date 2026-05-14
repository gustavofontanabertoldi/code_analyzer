import javalang
from utils.java_parser import parse_java_file

def analyze_complexity(path):
    count = 1

    try:
        tree = parse_java_file(path)
        for p, node in tree:
            if isinstance(node, javalang.tree.IfStatement):
                    count += 1
            
        return count
    except:
         return -1