def generate_results(results, duplications, benchmark, latency):
    print("\n===== RELATÓRIO FINAL =====\n")
    for result in results:
        print(f"Arquivo: {result['file']}")
        print(f"Complexity: {result['complexity']}")
        print(f"CBO: {result['cbo']}\n")

    print(f"Duplications: {duplications}")

    if benchmark == None:
        print(f"Benchmark: SKIPPED")
    else:
        print(f"Benchmark: {benchmark}\n")
    
    print("\n===== LATENCY =====\n")
    if latency == None:
        print(f"Latency: SKIPPED")
    else:
        for load, value in latency.items():
            print(f"Carga {load}: {value:.4f}")