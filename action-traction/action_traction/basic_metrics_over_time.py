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


def size_over_time(initial_data, repository_set):
    """Determine the size of a file over time and generate graph."""
    dataframe_list = []
    size_data = pd.DataFrame()

    # Iterate through every repo and generate a unique dataframe for each
    for repo in repository_set:
        new_data = initial_data.loc[initial_data['Repository'] == repo]
        # Remove unnecessary columns from dataframe
        new_data.drop(["Author", "Committer", "Branches", "Commit Message", "Lines Added", "Lines Removed", "Date of Change"], axis=1)
        dataframe_list.append(new_data)

    # Create comprehensive dataframe with size over every commit
    for dataframe in dataframe_list:
        size_data = size_data.append(dataframe)
    
    return size_data


def authors_over_time(initial_data, repository_set):
    """Determine the authors of a Actions file over time and generate graph."""
    dataframe_list = []
    author_data = pd.DataFrame()

    # Iterate through every repo and generate a unique dataframe for each
    for repo in repository_set:
        new_data = initial_data.loc[initial_data['Repository'] == repo]
        # Remove unnecessary columns from dataframe
        new_data.drop(["File Size in Bytes", "Committer", "Branches", "Commit Message", "Lines Added", "Lines Removed", "Date of Change"], axis=1)
        #TODO: Number of authors at one time
        dataframe_list.append(new_data)

    # Create comprehensive dataframe with authors over every commit
    for dataframe in dataframe_list:
        author_data = author_data.append(dataframe)
    
    return author_data


def committers_over_time(initial_data, repository_set):
    """Determine the committers of a Actions file over time and generate graph."""
    dataframe_list = []
    committer_data = pd.DataFrame()

    # Iterate through every repo and generate a unique dataframe for each
    for repo in repository_set:
        new_data = initial_data.loc[initial_data['Repository'] == repo]
        # Remove unnecessary columns from dataframe
        new_data.drop(["File Size in Bytes", "Author", "Branches", "Commit Message", "Lines Added", "Lines Removed", "Date of Change"], axis=1)
        #TODO: Number of committers at one time
        dataframe_list.append(new_data)

    # Create comprehensive dataframe with committers over every commit
    for dataframe in dataframe_list:
        committer_data = committer_data.append(dataframe)
    
    return committer_data


def lines_added_over_time(initial_data, repository_set):
    """Determine the lines added to a Actions file over time and generate graph."""
    dataframe_list = []
    added_data = pd.DataFrame()

    # Iterate through every repo and generate a unique dataframe for each
    for repo in repository_set:
        new_data = initial_data.loc[initial_data['Repository'] == repo]
        # Remove unnecessary columns from dataframe
        new_data.drop(["File Size in Bytes", "Author", "Branches", "Commit Message", "Committer", "Lines Removed", "Date of Change"], axis=1)
        dataframe_list.append(new_data)

    # Create comprehensive dataframe with lines added over every commit
    for dataframe in dataframe_list:
        added_data = added_data.append(dataframe)
    
    return added_data


def lines_removed_over_time(initial_data, repository_set):
    """Determine the lines removed from a Actions file over time and generate graph."""
    dataframe_list = []
    removed_data = pd.DataFrame()

    # Iterate through every repo and generate a unique dataframe for each
    for repo in repository_set:
        new_data = initial_data.loc[initial_data['Repository'] == repo]
        # Remove unnecessary columns from dataframe
        new_data.drop(["File Size in Bytes", "Author", "Branches", "Commit Message", "Committer", "Lines Removed", "Date of Change"], axis=1)
        dataframe_list.append(new_data)

    # Create comprehensive dataframe with lines removed over every commit
    for dataframe in dataframe_list:
        removed_data = removed_data.append(dataframe)
    
    return removed_data





