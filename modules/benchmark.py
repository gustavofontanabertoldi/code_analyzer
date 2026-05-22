import time
import requests
from config import SERVER_URL

def run_benchmark(endpoint, server_url=SERVER_URL):
    try:
        init = time.time()
        response = requests.get(
            f"{server_url}{endpoint}",
            timeout=10
        )
        print(f"Status Code do Benchmark: {response.status_code}")
        end = time.time()
        latency = end - init
        print(f"Latência -> {latency:.4f} segundos")
        return latency

    except Exception as e:
        print(f"Erro no benchmark: {e}")
        return -1
