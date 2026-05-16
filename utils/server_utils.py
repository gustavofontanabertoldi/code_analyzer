import subprocess
import time
import requests

from config import DEFAULT_ENDPOINT, SERVER_URL

def init_server(repo_path):
    process = subprocess.Popen(
        ["mvn.cmd", "spring-boot:run"],
        cwd = repo_path
    )

    url = f"{SERVER_URL}{DEFAULT_ENDPOINT}"

    for _ in range(60):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code < 500:
                print("Servidor iniciado com sucesso!\n")
                return process
        except:
            pass
    
        if process.poll() is not None:
            print("Servidor falhou ao iniciar!\n")
            return None
        time.sleep(1)
    
    print("Timeout do servidor.\n")
    return process

def stop_server(process):
    if process:
        process.terminate()