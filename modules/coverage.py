import os
from utils.file_utils import find_java_files
from config import REPO_DIR

def analyze_coverage():
    files = find_java_files(REPO_DIR)
    test_files = 0
    
    for file_path in files:
        file_name = os.basename(file_path)
        root_dir = os.path.dirname(file_path)
        
        file_lower = file_name.lower()
        root_lower = root_dir.lower()
        
        is_test_file = (
            file_name.endswith("Test.java")
            or file_name.endswith("Tests.java")
            or "test" in file_lower
            or "test" in root_lower
        )
        
        if is_test_file:
            test_files += 1
        
    total_java_files = len(files)
    if total_java_files == 0:
        coverage = 0.0
    else:
        coverage = (test_files/total_java_files) * 100
    
    return {
        "test_files":test_files,
        "total_java_files":total_java_files,
        "coverage": coverage
    }