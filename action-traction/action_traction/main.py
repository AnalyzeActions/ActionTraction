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
def basic_analysis(directory: str, analysis_selections: List[str]):
    """ Perform basic analysis of GitHub repositories (options: Modifiers, Size, Diff)"""
    # Analyze everything in a certain directory
    # If told otherwise, do the paths which are provided
    dataframe = traverse_repos.iterate_through_directory(directory)
    repo_set = basic.determine_repositories(dataframe)
    repo_file_dictionary = basic.determine_files_per_repo(dataframe, repo_set)
    basic.perform_specified_summarization(analysis_selections, dataframe)
# @app.command()
# def perform_summarization(User_selection: List[str]):
    

