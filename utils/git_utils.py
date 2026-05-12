from git import Repo
from git.exc import GitCommandError
import shutil
import os

def clone_repo(url, destination="temp/repo"):
    try:
        if os.path.exists(destination):
            shutil.rmtree(destination)

        #clona o repo
        Repo.clone_from(url, destination)
        print(f"repositório clonado em {destination}!\n")
    except GitCommandError:
        print("Erro ao clonar repositório!\n")