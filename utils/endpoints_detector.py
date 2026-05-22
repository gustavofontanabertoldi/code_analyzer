import re


def normalize_endpoint(endpoint):
    if not endpoint:
        return "/"
    endpoint = endpoint.strip()
    if not endpoint.startswith("/"):
        endpoint = f"/{endpoint}"
    return endpoint


def detect_endpoint(java_files):
    candidates = []
    
    for file in java_files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
            
            mappings = re.findall(
                r'@(GetMapping|RequestMapping)\("([^"]+)"\)',
                content
            )
            
            for _, endpoint in mappings:
                candidates.append(normalize_endpoint(endpoint))

            path_mappings = re.findall(r'@Path\("([^"]+)"\)', content)
            for endpoint in path_mappings:
                candidates.append(normalize_endpoint(endpoint))
        except Exception as e:
            print(f"Erro ao ler arquivo {file}: {e}")
        
    if candidates:
        return candidates[0]
    return "/"
