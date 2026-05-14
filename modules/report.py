def generate_results(results, duplications, benchmark, latency):
    print("\n===== RELATÓRIO FINAL =====\n")
    for result in results:
        print(f"Arquivo: {result['file']}")
        print(f"Complexity: {result['complexity']}")
        print(f"CBO: {result['cbo']}")

    print(f"Duplications: {duplications}")
    print(f"Benchmark: {benchmark}\n")
    
    print("\n===== LATENCY =====\n")
    for load, value in latency.items():
        print(f"Carga {load}: {value:.4f}")