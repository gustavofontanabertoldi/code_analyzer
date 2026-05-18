import time
import requests
from concurrent.futures import ThreadPoolExecutor
from config import SERVER_URL
from utils.endpoints_detector import detect_endpoint

def request():
    endpoint = detect_endpoint()
    return requests.get(
        f"{SERVER_URL}{endpoint}",
        timeout=10
    )

def analyze_latency():
    loads = [100, 500, 1000]
    results = {}

    for load in loads:
        try:
            init = time.time()
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = [
                    executor.submit(request)
                    for _ in range(load)
                ]

                for future in futures:
                    future.result()

            end = time.time()
            total = end - init
            average = total / load
            results[load] = average

        except Exception as e:
            print(f"Erro carga {load}: {e}")

    return results