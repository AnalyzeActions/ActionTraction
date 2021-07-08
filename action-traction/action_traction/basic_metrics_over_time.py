from pydriller import RepositoryMining
from typing import List
import pandas as pd
import datetime

def determine_repositories(initial_data):
    """Find each repository in the complete dataset of repository information."""
    # Create a list of all repositories
    repository_list = initial_data["Repository"].tolist()
    # Find each unique repository name return the set
    repository_set = set(repository_list)
    
    return repository_set


def determine_files_per_repo(initial_data, repository_set):
    """Determine all GitHub Actions files for a specific repository."""
    repo_file_dict = {}
    
    # Iterate through each unique repository name in the set
    for repository in repository_set:
        # Create a new dataset for each unique repository
        new_data = initial_data.loc[initial_data['Repository'] == repository]
        # Make a list of each of the files for a unique repository
        file_list = new_data["File"].tolist()
        # Determine each unique GitHub Actions file associated with a repository
        file_set = set(file_list)
        # Create a dictionary with repository as key and corresponding files as value
        repo_file_dict[repository] = file_set

    return repo_file_dict


def size_over_time(initial_data, repo_file_dict):
    """Determine the size of a file over time and generate graph."""
    size_dict = {}
    final_dict = {}
    dataframe_list = []
    size_dataframe = pd.DataFrame()

    # Iterate thorugh dictionary with repositories and corresponding files
    for repo, file_list in repo_file_dict.items():
        # Iterate through each file in a unique repository
        for file in file_list:
            # Create a new dataset for each file in a repo
            new_data = initial_data.loc[initial_data['File'] == file]
            size_list = new_data["File Size in Bytes"].tolist

            # TODO: Generate dataframe with index corresponding to size for each repo/file
            # TODO: Use indexes to then create the graph (on commit one size was ______ ) for each repo/file
            # TODO: Will allow us to compare file size for multiple repos over time (but not with time on x-axis, as times are different for repo commits)