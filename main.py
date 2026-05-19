from utils.git_utils import clone_repo
from utils.file_utils import find_java_files
from utils.server_utils import init_server, stop_server
from utils.project_detector import detect_database_usage
from utils.endpoints_detector import detect_endpoint

from modules.complexity import analyze_complexity
from modules.coupling import analyze_cbo
from modules.duplication import analyze_duplication
from modules.benchmark import run_benchmark
from modules.report import generate_results
from modules.latency import analyze_latency
from modules.coverage import analyze_coverage

from config import REPO_DIR

# Pega o link do repositório
url = input("Coloque a url do repositório: ")

#clona o repositório na máquina/projeto (Conferir em utils/git_utils)
clone_repo(url)

#Filtra os arquivos .java de outros arquivos (Conferir utils/file_utils)
java_files = find_java_files(REPO_DIR)

#Detecta endpoint para testes dinamicos
endpoint_alvo = detect_endpoint(java_files)

#lista de dados das análises dos arquivos.java
results = []

#Faz as verificações do código dos arquivos .java
for file in java_files:

    #Conferir modules/complexity e modules/coupling
    complexity = analyze_complexity(file)
    cbo = analyze_cbo(file)

    data = {
        "file":file,
        "complexity": complexity,
        "cbo": cbo
    }
    results.append(data)

#Confere as duplicações arquivo por arquivo e guarda (conferir modules/duplications)
duplications = analyze_duplication(java_files)

#Analisa o coverage
coverage = analyze_coverage()

db_required = detect_database_usage(REPO_DIR)

#Faz os testes de latencia do servidor java/spring-boot
process = None
if db_required:
    print(f"Projeto requer banco de dados")
else:
    process = init_server(REPO_DIR, endpoint_alvo)

benchmark = None
latency = None

if process:
    try:
        #Conferir modules/benchmark e modules/latency
        benchmark = run_benchmark(endpoint_alvo)
        latency = analyze_latency(endpoint_alvo)
    finally:
        stop_server(process)
else:
    print("Benchmark ignorado porque o servidor não iniciou.")

#Apresenta as infos
generate_results(results, duplications, benchmark, latency, coverage)