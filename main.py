from utils.git_utils import clone_repo
from utils.file_utils import find_java_files

from modules.complexity import analyze_complexity
from modules.coupling import analyze_cbo

url = input("Coloque a url do repositório: ")
clone_repo(url)

java_files = find_java_files("temp/repo")

for file in java_files:
    complexity = analyze_complexity(file)
    cbo = analyze_cbo(file)

    print(f"{file}")
    print(f"complexidade: {complexity}")
    print(f"CBO -> {cbo}\n")