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
def basic_analysis(directory: str):
    """ Perform basic analysis of GitHub repositories."""
    # Analyze everything in a certain directory
    # If told otherwise, do the paths which are provided
    dataframe = traverse_repos.iterate_through_directory(directory)
    typer.echo(dataframe)

    

@app.command()
def determine_metrics():
    """Determine user specified metrics to run"""
    typer.echo("Determining metrics to run")

