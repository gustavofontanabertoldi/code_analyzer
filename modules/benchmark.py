import time
import requests
from config import DEFAULT_ENDPOINT, SERVER_URL

def run_benchmark():
    try:
        init = time.time()
        response = requests.get(
            f"{SERVER_URL}{DEFAULT_ENDPOINT}",
            timeout=10
        )
        print(response.status_code)
        end = time.time()
        latency = end - init
        print(f"Latência -> {latency:.4f} segundos")
        return latency

    except Exception as e:
        print(f"Erro no benchmark: {e}")
        return -1