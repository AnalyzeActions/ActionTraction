from action_traction import download_repos
from typing import List
from pathlib import Path
import typer

app = typer.Typer()

# @app.callback()
# def callback():
#     """ Action Traction"""

@app.command()
def download_repositories(repositories: List, directory: Path):
    """ Import GitHub repository credentials"""
    download_repos.download_https(repositories, directory)

@app.command()
def determine_metrics():
    """Determine user specified metrics to run"""
    typer.echo("Determining metrics to run")

