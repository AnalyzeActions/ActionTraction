from action_traction import download_repos
from action_traction import traverse_repos
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
def basic_analysis(repositories: List[str], directory: Path):
    repositories_list = download_repos.generate_save_path(repositories, directory)
    for repository in repositories_list:
        files_changed_list = traverse_repos.generate_file_list(repository)
        actions_files = traverse_repos.determine_actions_files(files_changed_list)
        traverse_repos.iterate_actions_files(repository, actions_files)
    

@app.command()
def determine_metrics():
    """Determine user specified metrics to run"""
    typer.echo("Determining metrics to run")

