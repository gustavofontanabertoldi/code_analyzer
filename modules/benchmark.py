import time
import requests
from config import SERVER_URL
from utils.endpoints_detector import detect_endpoint

def run_benchmark():
    endpoint = detect_endpoint()
    try:
        init = time.time()
        response = requests.get(
            f"{SERVER_URL}{endpoint}",
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