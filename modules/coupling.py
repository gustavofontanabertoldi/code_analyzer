import javalang
from utils.java_parser import parse_java_file

def analyze_cbo(path):
    used_classes = set()
    try:
        tree = parse_java_file(path)

        for p, node in tree:
            if isinstance(node, javalang.tree.FieldDeclaration):
                tipo = node.type.name
                used_classes.add(tipo)
            if isinstance(node, javalang.tree.Import):
                used_classes.add(node.path)
            if isinstance(node, javalang.tree.ClassCreator):
                tipo = node.type.name
                used_classes.add(tipo)
        
        return len(used_classes)
    except:
        return -1