import subprocess
import time
import requests
import os

from config import (
    DEFAULT_ENDPOINT,
    SERVER_URL,
    JAVA_PATHS
)

from utils.project_detector import (
    detect_spring_boot_version,
    choose_java_version
)

def init_server(repo_path):

    spring_version = detect_spring_boot_version(repo_path)

    print(f"Spring Boot detectado: {spring_version}")

    java_version = choose_java_version(spring_version)

    print(f"Usando Java {java_version}")

    java_home = JAVA_PATHS.get(java_version)

    env = os.environ.copy()

    if java_home:
        env["JAVA_HOME"] = java_home
        env["PATH"] = f"{java_home}\\bin;" + env["PATH"]

    process = subprocess.Popen(
        ["mvn.cmd", "spring-boot:run"],
        cwd=repo_path,
        env=env
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