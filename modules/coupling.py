import javalang
from utils.java_parser import parse_java_file

PRIMITIVOS_E_WRAPPERS = {
    'int', 'long', 'double', 'float', 'short', 'byte', 'char', 'boolean', 'void',
    'String', 'Integer', 'Long', 'Double', 'Float', 'Short', 'Byte', 'Character', 'Boolean'
}

def analyze_cbo(path):
    used_classes = set()
    try:
        tree = parse_java_file(path)

        for _, node in tree:
            # 1. Atributos da Classe
            if isinstance(node, javalang.tree.FieldDeclaration):
                if hasattr(node.type, 'name'):
                    used_classes.add(node.type.name)
            
            # 2. Instanciações diretas (new MinhaClasse())
            elif isinstance(node, javalang.tree.ClassCreator):
                if hasattr(node.type, 'name'):
                    used_classes.add(node.type.name)
            
            # 3. Parâmetros de Métodos
            elif isinstance(node, javalang.tree.MethodDeclaration):
                # Tipo de Retorno
                if node.return_type and hasattr(node.return_type, 'name'):
                    used_classes.add(node.return_type.name)
                # Parâmetros de entrada
                for param in node.parameters:
                    if hasattr(param.type, 'name'):
                        used_classes.add(param.type.name)
            
            # 4. Herança e Interfaces (extends / implements)
            elif isinstance(node, javalang.tree.ClassDeclaration):
                if node.extends and hasattr(node.extends, 'name'):
                    used_classes.add(node.extends.name)
                if node.implements:
                    for impl in node.implements:
                        if hasattr(impl, 'name'):
                            used_classes.add(impl.name)

        filtered_classes = {cls for cls in used_classes if cls not in PRIMITIVOS_E_WRAPPERS}
        
        return len(filtered_classes)
    except Exception as e:
        print(f"Erro: {e}")
        return -1