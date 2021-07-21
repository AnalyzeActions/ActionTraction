"""A python program to download repositories from GitHub URLs."""
from typing import List
from pathlib import Path
import pandas as pd
import pathlib
import os
import git

from action_traction import constants
from rich.console import Console
from rich.progress import BarColumn
from rich.progress import Progress
from rich.progress import TimeRemainingColumn
from rich.progress import TimeElapsedColumn

from giturlparse import parse


def generate_save_path(repository_csv: Path, save_path: Path):
    """Generate each path that a repo should be saved to based on its name."""
    final_repository_paths = []
    converted_data = pd.read_csv(str(repository_csv))
    repository_list = converted_data["url"].tolist()
    for repo in repository_list:
        if parse(repo).valid:
            parsed_url = parse(repo)
            organization = parsed_url.owner
            repository_name = parsed_url.repo
        # else:
        #     organization = None
        #     repository_name = None

        repository_definition = organization + "." + repository_name
        
        path = pathlib.Path.home() / save_path / repository_definition

        final_repository_paths.append(str(path))

    # print(final_repository_paths)
    return final_repository_paths


def download_https(repository_csv: Path, path_list: List):
    """Download repositories using https URLs."""
    converted_data = pd.read_csv(str(repository_csv))
    repository_links = converted_data["url"].tolist()
    count = 0
    with Progress(
        constants.progress.Task_Format,
        BarColumn(),
        constants.progress.Percentage_Format,
        constants.progress.Completed,
        "•",
        TimeElapsedColumn(),
        "elapsed",
        "•",
        TimeRemainingColumn(),
        "remaining",
    ) as progress:
        download_task = progress.add_task("Download", total=len(repository_links))
        print("")
        # Clone a remote repository using https
        for x in range(0, len(repository_links)):
            git.Repo.clone_from(repository_links[x], path_list[x])
            count = count + 1
            progress.update(download_task, advance = 1)
        print("")