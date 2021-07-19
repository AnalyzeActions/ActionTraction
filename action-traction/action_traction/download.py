"""A python program to download repositories from GitHub URLs."""
from typing import List
from pathlib import Path
import pandas as pd
import pathlib
import os
import git


def generate_save_path(repository_csv: str, save_path: Path):
    """Generate each path that a repo should be saved to based on its name."""
    final_repository_paths = []
    converted_data = pd.read_csv(repository_csv)
    repository_list = converted_data["url"].tolist()
    for repo in repository_list:
        repo_name = os.path.splitext(os.path.basename(repo))[0]
        path = pathlib.Path.home() / save_path / repo_name
        final_repository_paths.append(str(path))

    # print(final_repository_paths)
    return final_repository_paths


def download_https(repository_csv: str, path_list: List):
    """Download repositories using https URLs."""
    converted_data = pd.read_csv(repository_csv)
    repository_links = converted_data["url"].tolist()
    count = 0
    # Clone a remote repository using https
    for x in range(0, len(repository_links)):
        git.Repo.clone_from(repository_links[x], path_list[x])
        count = count + 1
