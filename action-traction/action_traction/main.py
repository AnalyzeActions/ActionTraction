from action_traction import download_repos
from action_traction import traverse_repos
from action_traction import basic_analysis_calculations as basic
from typing import List
from pathlib import Path
import typer

app = typer.Typer()

# @app.callback()
# def callback():
#     """ Action Traction"""

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
def basic_analysis(directory: str, analysis_selections: List[str]):
    """ Perform basic analysis of GitHub repositories (options: Modifiers, Size, Diff)"""
    basic.perform_specified_summarization(analysis_selections, directory)
# @app.command()
# def perform_summarization(User_selection: List[str]):
    

