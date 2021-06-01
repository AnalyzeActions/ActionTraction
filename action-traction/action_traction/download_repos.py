from typing import List 
from pathlib import Path
import pathlib
import os
import git

def generate_save_path(repository_list: List, save_path: Path):
    final_repository_paths = []
    for repo in repository_list:
        repo_name = os.path.splitext(os.path.basename(repo))[0]
        path = pathlib.Path.home() / save_path / repo_name
        final_repository_paths.append(path)
    
    return final_repository_paths

def download_https(repository_list: List, path_list: List):
    count = 0
    # Clone a remote repository using https
    for x in range(0, len(repository_list)-1):
        git.Repo.clone_from(repository_list[x], path_list[x])
        count = count + 1
    
    return count

#TODO: tmpfs fixture to test download_https
