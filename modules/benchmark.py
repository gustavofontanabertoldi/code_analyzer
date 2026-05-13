import subprocess
import time
import requests

def run_benchmark(repo_path):
    try:
        process = subprocess.Popen(
            ["mvn", "spring-boot:run"],
            cwd=repo_path
        )
        time.sleep(15)
        init = time.time()
        requests.get(
            "http://localhost:8080",
            timeout=10
        )
        end = time.time()
        latency = end - init
        print(f"Latência -> {latency:.4f} segundos")
        process.terminate()
        return latency

    except Exception as e:
        print(f"Erro no benchmark: {e}")
        return -1