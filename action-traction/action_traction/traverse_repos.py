"""A python program to traverse repositories in a given directory and generate datasets with all relevant information."""
from pydriller import Repository
from typing import List
import pandas as pd
import os
import pathlib


def generate_file_list(repository_path: str):
    """Generate a list of .yml files in a repository."""
    files_changed_list = []
    # Iterate through all of the commits in a repository, and find all modified .yml files
    for commit in Repository(
        repository_path, only_modifications_with_file_types=[".yml"]
    ).traverse_commits():
        for changed_file in commit.modified_files:
            files_changed_list.append(changed_file.new_path)

    return files_changed_list


def determine_actions_files(modified_files: List[str]):
    """Generate a list of GitHub Actions files in a repository."""
    files_to_analyze = []
    # Iterate through list of modified files
    for file in modified_files:
        # Determine if the file is a GitHub Actions workflow file
        if ".github" in str(file):
            # If Action file, add to a specific list of files to analyze
            if files_to_analyze.count(str(file)) == 0:
                files_to_analyze.append(str(file))

    return files_to_analyze


def iterate_actions_files(repository_path: str, files_to_analyze: List[str]):
    """Mine a repository and find metrics associated with GitHub Actions workflow files."""
    # Initalize all necessary lists
    author_list = []
    committer_list = []
    date_list = []
    branches_list = []
    commit_messages_list = []
    lines_added_list = []
    lines_deleted_list = []
    file_list = []
    repository_list = []
    size_bytes_list = []
    hash_list = []
    # Initialize dictionary for repository data
    raw_data = {}
    # Initialize pandas dataframes
    first_dataframe = pd.DataFrame()

    # Iterate through list of Actions files for a repository
    for file in files_to_analyze:
        # Iterate through the commits of a repository where a GitHub Actions file was modified
        for commit in Repository(repository_path, filepath=file).traverse_commits():
            # Create a complete path of the GitHub Actions file
            complete_file = repository_path + "/" + file

            # Mine repository and add all metrics to corresponding list
            hash_list.append(commit.hash)
            file_list.append(file)
            repository_list.append(repository_path)
            author_list.append(commit.author.name)
            committer_list.append(commit.committer.name)
            date_list.append(commit.committer_date)
            commit_messages_list.append(commit.msg)
            size_bytes_list.append(os.stat(complete_file).st_size)
            lines_added_list.append(commit.insertions)
            lines_deleted_list.append(commit.deletions)

        # Create a dictionary for a repository and its corresponding metrics
        raw_data["hash"] = hash_list
        raw_data["repo"] = repository_list
        raw_data["file"] = file_list
        raw_data["size_bytes"] = size_bytes_list
        raw_data["author"] = author_list
        raw_data["committer"] = committer_list
        raw_data["commit_message"] = commit_messages_list
        raw_data["lines_added"] = lines_added_list
        raw_data["lines_removed"] = lines_deleted_list
        raw_data["date"] = date_list

    # Create a pandas dictionary for repository dictionary
    first_dataframe = pd.DataFrame.from_dict(raw_data, orient="columns")

    return first_dataframe


def iterate_entire_repo(repository_path: str):
    """Iterate through an entire repository and generate a complete dataframe of relevant metrics."""
    hash_list = []
    date_list = []
    author_list = []
    repository_list = []
    files_changed_list = []
    raw_data = {}

    # Iterate through every commit in a repository
    for commit in Repository(repository_path).traverse_commits():

        # Iterate through modified files in a commit and generate a list of names
        for mod in commit.modified_files:
            files_changed_list.append(mod.filename)
            hash_list.append(commit.hash)
            date_list.append(commit.committer_date)
            author_list.append(commit.author.name)
            repository_list.append(repository_path)
            entire_repo_data = pd.DataFrame()

        # Create a dictionary with information relating to the entire repository
    raw_data["hash"] = hash_list
    raw_data["date"] = date_list
    raw_data["repo"] = repository_list
    raw_data["author"] = author_list
    raw_data["files_changed"] = files_changed_list

    # Create a pandas dataframe from the raw dictionary
    entire_repo_data = pd.DataFrame.from_dict(raw_data, orient="columns")

    return entire_repo_data


def combine_rows_whole_repo(entire_repo_data):
    """Combine rows with the same hash in the entire repository dataframe."""
    hash_list = entire_repo_data["hash"].tolist()
    hash_set = set(hash_list)
    hash_dict = {}
    complete_dataframe = pd.DataFrame()

    # Iterate through commit hashes and create new datasets for each
    for commit_hash in hash_set:
        new_data = entire_repo_data.loc[entire_repo_data["hash"] == commit_hash]
        modified_files = new_data["files_changed"].tolist()

        repositories_list = new_data["repo"].tolist()
        repo_name = repositories_list[0]

        hash_dict[(commit_hash, repo_name)] = modified_files

        complete_dataframe = pd.DataFrame.from_dict(hash_dict)

    print(complete_dataframe)
    # repositories_list = new_data["Repository"].tolist()
    # repo_name = repositories_list[0]

    # hash_dict["Hash"] = [commit_hash]
    # hash_dict["Repository"] = [repo_name]
    # hash_dict["Modified Files"] = modified_files

    # hash_data = pd.DataFrame.from_dict(hash_dict)

    # dictionary_list.append(hash_data)

    # for dictionary in dictionary_list:
    #     complete_dictionary = complete_dictionary.append(dictionary)

    # print(complete_dictionary)


def iterate_through_directory(root_directory: str):
    """Generate a comprehensive dataframe of metrics for each repository in a specified directory."""
    repos_to_check = []
    dataframes_list = []
    entire_repo_list = []
    final_dataframe = pd.DataFrame()
    entire_repo_dataframe = pd.DataFrame()

    # Generate a list of each subdirectory in the specified root directory
    for subdir, dirs, files in os.walk(root_directory):
        repos_to_check.append(dirs)

    # Iterate through each repository and perform methods to generate metrics
    for repository in repos_to_check[0]:
        path = pathlib.Path.home() / root_directory / repository
        all_files_changed = generate_file_list(str(path))
        actions_files = determine_actions_files(all_files_changed)
        single_repo_dataframe = iterate_actions_files(str(path), actions_files)
        # Add each repository-specific dataframe to a list
        dataframes_list.append(single_repo_dataframe)
        # Iterate through repositories and generate a dataframe with info from each commit
        entire_repo_data = iterate_entire_repo(str(path))
        # Create a list of entire repo dataframes
        entire_repo_list.append(entire_repo_data)

    # Create a comprehensive dataframe with individual repo dataframes
    for initial_data in dataframes_list:
        final_dataframe = final_dataframe.append(initial_data)

    # Create a comprehensive dataframe with the entire repo dataframes
    for dataframe in entire_repo_list:
        entire_repo_dataframe = entire_repo_dataframe.append(dataframe)

    # Put dataframe information into a .csv file
    csv_path = root_directory + "/minedRepos.csv"
    entire_repo_path = root_directory + "/entireRepo.csv"
    print("Repository Mining Completed")
    final_dataframe.to_csv(csv_path)
    entire_repo_dataframe.to_csv(entire_repo_path)

    combine_rows_whole_repo(entire_repo_dataframe)
