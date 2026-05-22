import os

from utils.git_utils import clone_repo
from utils.file_utils import find_java_files
from utils.server_utils import init_server, stop_server
from utils.project_detector import (
    detect_database_usage,
    detect_project_framework,
    detect_server_url,
    prepare_h2_test_database,
)
from utils.endpoints_detector import detect_endpoint

from modules.complexity import analyze_complexity
from modules.coupling import analyze_cbo
from modules.duplication import analyze_duplication
from modules.benchmark import run_benchmark
from modules.report import generate_results
from modules.latency import analyze_latency
from modules.coverage import run_coverage_analysis

from config import REPO_DIR


try:
    url = input("Coloque a url do repositorio: ")
    clone_repo(url)

    java_files = find_java_files(REPO_DIR)
    if not java_files:
        print("[AVISO] Nenhum arquivo Java encontrado para analise.")
        java_files = []

    endpoint_alvo = detect_endpoint(java_files)

    results = []
    for file in java_files:
        complexity = analyze_complexity(file)
        cbo = analyze_cbo(file)
        results.append({
            "file": file,
            "complexity": complexity,
            "cbo": cbo,
        })

    duplications = analyze_duplication(java_files)

    db_info = detect_database_usage(REPO_DIR)
    framework = detect_project_framework(REPO_DIR)
    print(f"Framework detectado: {framework}")

    coverage = None
    benchmark = None
    latency = None
    h2_ready = False

    if db_info.has_database:
        print("[AVISO] Projeto com uso de banco detectado.")
        print(f"Fonte: {db_info.source} | Gatilho: {db_info.trigger}")

        if framework == "spring-boot":
            h2_ready = prepare_h2_test_database(REPO_DIR)
            if h2_ready:
                os.environ["SPRING_PROFILES_ACTIVE"] = "test"
                print("Perfil Spring ativo para execucao dinamica: test")
            else:
                print("Analise dinamica e cobertura podem falhar: nao foi possivel preparar o H2.")
                print("Execute o banco correspondente localmente para habilitar estas analises.")
        else:
            print("Patch automatico de H2 ignorado: suporte atual cobre apenas Spring Boot.")
            print("A analise dinamica seguira sem trocar o banco do projeto alvo.")

    can_try_dynamic = not db_info.has_database or h2_ready or framework != "spring-boot"

    if can_try_dynamic:
        server_url = detect_server_url(REPO_DIR)
        print(f"URL base detectada para o servidor: {server_url}")

        coverage = run_coverage_analysis(REPO_DIR)

        print("Iniciando o servidor em background para testes dinamicos...")
        process = init_server(REPO_DIR, endpoint_alvo, server_url)

        if process:
            try:
                print("Servidor iniciado com sucesso! Executando benchmarks...")
                benchmark = run_benchmark(endpoint_alvo, server_url)
                latency = analyze_latency(endpoint_alvo, server_url)
            finally:
                print("Finalizando o servidor em background...")
                stop_server(process)
        else:
            print("Falha critica: o processo do servidor nao pode ser iniciado.")
            print("Benchmark ignorado porque o servidor nao iniciou.")

    generate_results(results, duplications, benchmark, latency, coverage)

except Exception as e:
    print(f"Ocorreu um erro inesperado no fluxo principal: {e}")
