"""The command line interface for ActionTraction."""
from action_traction import download as down
from action_traction import traverse
from action_traction import basic_metrics as basic
from action_traction import contents_metrics as file_contents
from action_traction import complexity
from action_traction import summarization as summary
from action_traction import new_traverse as new
from action_traction import new_complexity
from action_traction import join
from typing import List
from pathlib import Path
import typer
import pandas as pd

app = typer.Typer()


@app.command()
def download(repositories: Path, directory: Path):
    """Import GitHub repository credentials."""
    path_list = down.generate_save_path(repositories, directory)
    number_repos = down.download_https(repositories, path_list)


@app.command()
def traverse_repos(directory: str):
    """Generate a .csv file for all given repositories."""
    new.iterate_through_directory(directory)


@app.command()
def analyze(directory_path: str):
    final_dataset = basic.combine_dataframes(directory_path)
    new_complexity.iterate_through_directory(directory_path)
    dataset = file_contents.contents_over_time(directory_path)
    summary.github_actions_contributors(directory_path)
    summary.entire_repo_metrics(directory_path)

@app.command()
def join(path_one, path_two, key):
    join.join_datasets(path_one, path_two, key)