import subprocess
import time

def init_server(repo_path):
    process = subprocess.Popen(
        ["mvn", "spring-boot:run"],
        cwd = repo_path
    )

    time.sleep(15)
    return process

def stop_server(process):
    process.terminate()