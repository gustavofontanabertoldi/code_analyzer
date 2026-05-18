import os
import re
from utils.file_utils import find_java_files
from config import REPO_DIR

def detect_endpoint():
    candidates = []
    java_files = find_java_files(REPO_DIR)
    for file in java_files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
            
            mappings = re.findall(
                r'@(GetMapping|RequestMapping)\("([^"]+)"\)',
                content
            )
            
            for _, endpoint in mappings:
                candidates.append(endpoint)
        except Exception as e:
            print(f"Erro ao ler arquivo {file}: {e}")
        
    if candidates:
        return candidates[0]
    return "/"