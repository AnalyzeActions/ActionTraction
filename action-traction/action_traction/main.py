from action_traction import download_repos
from action_traction import traverse_repos
from action_traction import basic_analysis_calculations as basic
from action_traction import file_contents_analysis as actions_analysis
from action_traction import quality_score
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


@app.command()
def action_file_analysis(directory: str, analysis_selections: List[str]):
    # , csv_pathway: str
    # data = actions_analysis.iterate_through_directory(directory)
    # actions_analysis.generate_abstract_syntax_trees(data, csv_pathway)
    actions_analysis.perform_specified_analysis(directory, analysis_selections)


@app.command()
def determine_quality(repository_path: str, score_selection: List[str]):
    """Generate a quality score for GitHub Actions files."""
    quality_score.final_score(repository_path, score_selection)
