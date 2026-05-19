import time
import asyncio
import aiohttp
from config import SERVER_URL

async def fetch(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            await response.read()
            return response.status
    except Exception:
        return None

async def run_load_test(url, total_requests):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for _ in range(total_requests)]
        await asyncio.gather(*tasks)

# CORRIGIDO: Recebe o endpoint diretamente do Main
def analyze_latency(endpoint):
    url = f"{SERVER_URL}{endpoint}"
    
    loads = [100, 500, 1000]
    results = {}

    for load in loads:
        try:
            print(f"Disparando carga assíncrona de {load} requisições...")
            init = time.time()
            
            asyncio.run(run_load_test(url, load))
            
            end = time.time()
            total_time = end - init
            average = total_time / load
            results[load] = average
            
        except Exception as e:
            print(f"Erro carga {load}: {e}")

    return results