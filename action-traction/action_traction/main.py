from action_traction import download_repos
from action_traction import traverse_repos
from action_traction import basic_metrics_over_time as basic
from action_traction import complexity
from typing import List
from pathlib import Path
import typer

app = typer.Typer()

@app.command()
def download_repositories(repositories: List[str], directory: Path):
    """ Import GitHub repository credentials"""
    path_list = download_repos.generate_save_path(repositories, directory)
    number_repos = download_repos.download_https(repositories, path_list)

@app.command()
def generate_repository_metrics(directory: str):
    """Generate a .csv file for all given repositories."""
    traverse_repos.iterate_through_directory(directory)

@app.command()
def determine_diffs(directory:str):
    """Generate a understanding of the diffs of a GitHub Actions workflow."""
    final_dataset = basic.combine_dataframes(directory)

@app.command()
def determine_quality(directory_path: str):
    """Generate a quality score for GitHub Actions files."""
    complexity.iterate_through_directory(directory_path)
