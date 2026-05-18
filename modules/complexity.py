import javalang
from utils.java_parser import parse_java_file

def analyze_complexity(path):
    results = []

    try:
        tree = parse_java_file(path)

        for _, method in tree.filter(javalang.tree.MethodDeclaration):
            complexity = 1
            for _, node in method:
                if isinstance(node, javalang.tree.IfStatement):
                    complexity += 1
            
            results.append({
                "method": method.name,
                "complexity": complexity
            })
        
        return results
    except Exception as e:
        print(f"Erro complexidade: {e}")
        return []