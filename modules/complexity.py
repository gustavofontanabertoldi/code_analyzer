import os

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

            if complexity <= 10:
                status = "Baixo"
            elif complexity <= 20:
                status = "Médio"
            elif complexity <=50:
                status = "Alto"
            else:
                status = "Instável"
            
            results.append({
                "method": method.name,
                "complexity": complexity,
                "status": status
            })
        
        return results
    except Exception as e:
        message = str(e) or type(e).__name__
        print(f"Erro complexidade em {os.path.basename(path)}: {message}")
        return []
