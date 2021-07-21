"""The command line interface for ActionTraction."""
from action_traction import download as down
from action_traction import traverse
from action_traction import basic_metrics as basic
from action_traction import contents_metrics as file_contents
from action_traction import complexity
from action_traction import summarization as summary
from action_traction import join
from typing import List
from pathlib import Path
import typer

app = typer.Typer()


@app.command()
def download(repositories: Path, directory: Path):
    """Import GitHub repository credentials."""
    path_list = down.generate_save_path(repositories, directory)
    number_repos = down.download_https(repositories, path_list)


@app.command()
def repository_metrics(directory: str):
    """Generate a .csv file for all given repositories."""
    traverse.iterate_through_directory(directory)


@app.command()
def determine_diffs(directory: str):
    """Generate a understanding of the diffs of a GitHub Actions workflow."""
    final_dataset = basic.combine_dataframes(directory)


@app.command()
def determine_complexity(directory_path: str):
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

@app.command()
def whole_repo(directory_path: str):
    """Determine metrics for every commit in a GitHub repository."""
    summary.entire_repo_metrics(directory_path)

@app.command()
def join_data(directory_path: str):
    join.perform_joining(directory_path)

