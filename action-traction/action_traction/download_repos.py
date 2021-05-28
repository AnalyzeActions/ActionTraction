from typing import List 
from pathlib import Path
import pathlib
import os
import git

def download_https(repository_list: List, save_path: Path):
    # Clone a remote repository using https
    for repo in repository_list:
        repo_name = os.path.splitext(os.path.basename(repo))[0]
        # print(repo_name)
        path = pathlib.Path.home() / save_path / repo_name
        # path = save_path / repo_name
        git.Repo.clone_from(repo, path)
