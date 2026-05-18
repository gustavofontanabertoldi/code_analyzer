def generate_results(results, duplications, benchmark, latency, coverage):
    print("\n===== RELATÓRIO FINAL =====\n")
    print("\n===== CBO E COMPLEXIDADE=====\n")
    for result in results:
        print(f"Arquivo: {result['file']}")
        for method in result["complexity"]:
            print(f"Metodo: {method["method"]} - Complexidade: {method["complexity"]}")
        print(f"CBO: {result['cbo']}\n")
        
    print("\n===== DUPLICATIONS =====\n")
    print(f"Duplications: {duplications}\n")
    
    print("\n===== COVERAGE =====\n")

    print(
        f"Arquivos de teste: "
        f"{coverage['test_files']}\n"
    )
    print(
        f"Arquivos Java: "
        f"{coverage['total_java_files']}\n"
    )
    print(
        f"Cobertura estimada: "
        f"{coverage['coverage']}%\n"
    )

    if benchmark == None:
        print(f"Benchmark: SKIPPED")
    else:
        print(f"Benchmark: {benchmark}")
    
    print("\n===== LATENCY =====\n")
    if latency == None:
        print(f"Latency: SKIPPED")
    else:
        for load, value in latency.items():
            print(f"Carga {load}: {value:.4f}")