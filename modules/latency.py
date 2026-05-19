# modules/latency

import time
import asyncio
import aiohttp
from config import SERVER_URL

async def fetch(session, url):
    try:
        async with session.get(url, timeout=15) as response:
            await response.read()
            return response.status
    except Exception:
        return None

async def run_load_test(url, total_requests):
    connector = aiohttp.TCPConnector(limit=None)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch(session, url) for _ in range(total_requests)]
        await asyncio.gather(*tasks)

def analyze_latency(endpoint):
    url = f"{SERVER_URL}{endpoint}"
    
    loads = [100, 500, 1000, 5000]
    raw_times = {}

    # 1. Executa os testes e coleta os tempos brutos de execução
    for load in loads:
        try:
            print(f"Disparando carga assíncrona de {load} requisições...")
            init = time.time()
            
            asyncio.run(run_load_test(url, load))
            
            end = time.time()
            total_time = end - init
            
            # Guardamos o tempo total que levou para processar aquele lote
            raw_times[load] = total_time
            
        except Exception as e:
            print(f"Erro carga {load}: {e}")
            raw_times[load] = None

    results = {}
    base_load = 100
    base_time = raw_times.get(base_load)

    if base_time:
        for load, total_time in raw_times.items():
            if total_time is None:
                results[load] = {"avg_time": -1, "percent_increase": -1}
                continue

            avg_time = total_time / load
            
            # Cálculo do % de aumento em relação à carga base de 100
            if load == base_load:
                percent_increase = 0.0
            else:
                percent_increase = ((total_time - base_time) / base_time) * 100

            results[load] = {
                "avg_time": avg_time,
                "percent_increase": percent_increase
            }
    else:
        print("Não foi possível estabelecer a carga base de 100 requisições.")

    return results