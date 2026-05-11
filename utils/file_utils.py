import os

def find_java_files(repo_path):
    java_files = []

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".java"):
                full_path = os.path.join(root, file)
                java_files.append(full_path)
    
    return java_files