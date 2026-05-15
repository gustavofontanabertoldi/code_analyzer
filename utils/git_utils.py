from git import Repo
from git.exc import GitCommandError
import shutil
import os
from config import REPO_DIR

def clone_repo(url):
    try:
        if os.path.exists(REPO_DIR):
            shutil.rmtree(REPO_DIR)

        os.makedirs(REPO_DIR, exist_ok=True)
        #clona o repo
        Repo.clone_from(url, REPO_DIR)
        print(f"repositório clonado em {REPO_DIR}!\n")
    except GitCommandError:
        print("Erro ao clonar repositório!\n")