from git import Repo
from git.exc import GitCommandError
import shutil
import os
import stat
from config import REPO_DIR

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone_repo(url):
    try:
        if os.path.exists(REPO_DIR):
            shutil.rmtree(REPO_DIR, onexc=remove_readonly)

        os.makedirs(REPO_DIR, exist_ok=True)
        #clona o repo
        Repo.clone_from(url, REPO_DIR)
        print(f"repositório clonado em {REPO_DIR}!\n")
    except GitCommandError:
        print("Erro ao clonar repositório!\n")