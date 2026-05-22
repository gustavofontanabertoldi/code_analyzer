import os
import subprocess
import time

import requests

from config import JAVA_PATHS, SERVER_URL, TEMP_DIR
from utils.project_detector import (
    choose_java_version,
    detect_project_framework,
    detect_server_url,
    detect_spring_boot_version,
    validate_java_compatibility,
)


def init_server(repo_path, endpoint, server_url=None):
    java_ok, required_java, current_java = validate_java_compatibility(repo_path)
    if not java_ok:
        print(
            "Servidor nao iniciado: o projeto exige "
            f"Java {required_java}, mas o Java atual e {current_java}."
        )
        return None

    framework = detect_project_framework(repo_path)
    print(f"Framework detectado: {framework}")

    spring_version = detect_spring_boot_version(repo_path)
    print(f"Spring Boot detectado: {spring_version}")

    java_version = choose_java_version(spring_version)
    print(f"Usando Java {java_version}")

    java_home = JAVA_PATHS.get(java_version)
    env = os.environ.copy()

    if java_home and os.path.exists(java_home):
        env["JAVA_HOME"] = java_home
        env["PATH"] = f"{java_home}\\bin;" + env["PATH"]
    elif java_home:
        print(f"[AVISO] JAVA_HOME configurado nao existe: {java_home}. Usando Java do sistema.")

    os.makedirs(TEMP_DIR, exist_ok=True)
    log_path = os.path.join(TEMP_DIR, "server.log")

    command = ["mvn.cmd", "spring-boot:run"]
    if framework == "quarkus":
        command = ["mvn.cmd", "quarkus:dev"]
    elif framework != "spring-boot":
        print("Servidor dinamico ignorado: framework Maven generico sem comando de start conhecido.")
        return None

    with open(log_path, "w", encoding="utf-8") as log_file:
        process = subprocess.Popen(
            command,
            cwd=repo_path,
            env=env,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True,
        )

    base_url = server_url or detect_server_url(repo_path) or SERVER_URL
    url = f"{base_url}{endpoint}"
    print(f"Monitorando servidor em: {url}")

    for _ in range(60):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code < 500:
                print("Servidor iniciado com sucesso!\n")
                return process
        except requests.RequestException:
            pass

        if process.poll() is not None:
            print("Servidor falhou ao iniciar!\n")
            print(f"Consulte o log em: {log_path}")
            return None

        time.sleep(1)

    print("Timeout do servidor.\n")
    print(f"Consulte o log em: {log_path}")
    return None


def stop_server(process):
    if process:
        process.terminate()
