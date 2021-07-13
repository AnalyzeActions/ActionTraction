"""A python program to download repositories from GitHub URLs."""
from typing import List
from pathlib import Path
import pathlib
import os
import git


def generate_save_path(repository_list: List, save_path: Path):
    """Generate each path that a repo should be saved to based on its name."""
    final_repository_paths = []
    for repo in repository_list:
        repo_name = os.path.splitext(os.path.basename(repo))[0]
        path = pathlib.Path.home() / save_path / repo_name
        final_repository_paths.append(str(path))

    # print(final_repository_paths)
    return final_repository_paths


def download_https(repository_list: List, path_list: List):
    """Download repositories using https URLs."""
    count = 0
    # Clone a remote repository using https
    for x in range(0, len(repository_list)):
        git.Repo.clone_from(repository_list[x], path_list[x])
        count = count + 1
