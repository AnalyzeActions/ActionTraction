"""A python program to determine basic metrics of GitHub Actions configuration over time."""
import pandas as pd
from ordered_set import OrderedSet


def determine_repositories(initial_data):
    """Find each repository in the complete dataset of repository information."""
    # Create a list of all repositories
    repository_list = initial_data["repo"].tolist()
    # Find each unique repository name return the set
    repository_set = OrderedSet(repository_list)

    return repository_set


def size_over_time(initial_data, repository_set):
    """Determine the size of a file over time and generate graph."""
    dataframe_list = []
    size_data = pd.DataFrame()

    # Iterate through every repo and generate a unique dataframe for each
    for repo in repository_set:
        new_data = initial_data.loc[initial_data["repo"] == repo]
        # Remove unnecessary columns from dataframe
        new_data.drop(
            new_data.columns[[0, 3, 6, 7, 10, 11, 12]], axis=1, inplace=True
        )
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
        new_data = initial_data.loc[initial_data["repo"] == repo]
        # Remove unnecessary columns from dataframe
        new_data.drop(
            new_data.columns[[0, 3, 6, 7, 9, 11, 12]], axis=1, inplace=True
        )
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
        new_data = initial_data.loc[initial_data["repo"] == repo]
        # Remove unnecessary columns from dataframe
        new_data.drop(new_data.columns[[0, 3, 6, 7, 9, 10, 12]], axis=1, inplace=True)
        dataframe_list.append(new_data)

    # Create comprehensive dataframe with lines removed over every commit
    for dataframe in dataframe_list:
        removed_data = removed_data.append(dataframe)

    return removed_data


def combine_dataframes(directory):
    """Combine all dataframes with basic metrics to generate one significant dataframe."""
    initial_data_path = directory + "/final_data.csv"
    initial_data = pd.read_csv(initial_data_path)

    repository_set = determine_repositories(initial_data)
    final_dataset = pd.DataFrame()
    size_data = size_over_time(initial_data, repository_set)

    added_data = lines_added_over_time(initial_data, repository_set)

    removed_data = lines_removed_over_time(initial_data, repository_set)

    lines_added_list = added_data["lines_added"].tolist()
    lines_removed_list = removed_data["lines_removed"].tolist()

    final_dataset = size_data
    final_dataset["lines_added"] = lines_added_list
    final_dataset["lines_removed"] = lines_removed_list

    final_dataset_path = directory + "/diffs.csv"
    final_dataset.to_csv(final_dataset_path)
    return final_dataset
