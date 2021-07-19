"""The command line interface for ActionTraction."""
from action_traction import download
from action_traction import traverse
from action_traction import basic_metrics_over_time as basic
from action_traction import file_contents_analysis as file_contents
from action_traction import complexity
from action_traction import summarization as summary
from typing import List
from pathlib import Path
import typer

app = typer.Typer()


@app.command()
def download_repositories(repositories: str, directory: Path):
    """Import GitHub repository credentials."""
    path_list = download.generate_save_path(repositories, directory)
    number_repos = download.download_https(repositories, path_list)


@app.command()
def generate_repository_metrics(directory: str):
    """Generate a .csv file for all given repositories."""
    traverse_repos.iterate_through_directory(directory)


@app.command()
def determine_diffs(directory: str):
    """Generate a understanding of the diffs of a GitHub Actions workflow."""
    final_dataset = basic.combine_dataframes(directory)


@app.command()
def determine_quality(directory_path: str):
    """Generate a quality score for GitHub Actions files."""
    complexity.iterate_through_directory(directory_path)


@app.command()
def contents_analysis(directory_path: str):
    """Understand how the contents of GitHub Actions workflows change over time."""
    dataset = file_contents.contents_over_time(directory_path)


@app.command()
def contributors(directory_path: str):
    """Determine contributors for a repository and GitHub Actions.""" 
    summary.determine_contributors(directory_path)

# @app.command()
# def
