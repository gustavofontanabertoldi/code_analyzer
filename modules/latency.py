import time
import requests
from config import DEFAULT_ENDPOINT

def analyze_latency():
        loads = [100, 500, 1000]
        results = {}

        for load in loads:
            try:
                init = time.time()
                for i in range(load):
                    requests.get(
                        f"http://localhost:8080{DEFAULT_ENDPOINT}",
                        timeout=10
                    )
                end = time.time()
                latency = end - init
                average_latency = latency/load
                results[load] = average_latency
            except Exception as e:
                 print(f"Erro na carga {load}: {e}")
        return results