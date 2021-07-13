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


def combine_dataframes(directory):
    initial_data_path = directory + "/minedRepos.csv"
    initial_data = pd.read_csv(initial_data_path)
    repository_set = determine_repositories(initial_data)
    final_dataset = pd.DataFrame()
    size_data = size_over_time(initial_data, repository_set)
    added_data = lines_added_over_time(initial_data, repository_set)
    removed_data = lines_removed_over_time(initial_data, repository_set)

    lines_added_list = added_data["Lines Added"].tolist()
    lines_removed_list = removed_data["Lines Removed"].tolist()

    final_dataset = size_data
    final_dataset["Lines Added"] = lines_added_list
    final_dataset["Lines Removed"] = lines_removed_list

    final_dataset_path = directory + "/diffs.csv"
    final_dataset.to_csv(final_dataset_path)
    return final_dataset 
