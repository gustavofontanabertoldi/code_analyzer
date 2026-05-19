import os
from utils.file_utils import find_java_files
from config import REPO_DIR

def analyze_coverage():
    files = find_java_files(REPO_DIR)
    test_files = 0
    
    for file_path in files:
        rel_path = os.path.relpath(file_path, REPO_DIR)
        
        rel_path_normalized = rel_path.replace("\\", "/")
        
        is_test_file = (
            "src/test/java/" in rel_path_normalized 
            and rel_path_normalized.endswith(".java")
        )
        
        if is_test_file:
            test_files += 1
        
    total_java_files = len(files)
    if total_java_files == 0:
        coverage = 0.0
    else:
        coverage = (test_files / total_java_files) * 100
    
    return {
        "test_files": test_files,
        "total_java_files": total_java_files,
        "coverage": coverage
    }