from pydriller import Repository
import pandas as pd
import os
import pathlib

def traverse_all_commits(repository_path: str):
    hash_list = []
    date_list = []
    repository_list = []
    author_list = []
    committer_list = []
    files_changed_list = []
    size_list = []
    lines_added_list = []
    lines_removed_list = []

    raw_data = {}

    for commit in Repository(repository_path).traverse_commits():
        for modification in commit.modified_files:
            complete_file = repository_path + "/" + modification.filename

            hash_list.append(commit.hash)
            date_list.append(commit.committer_date)
            repository_list.append(repository_path)
            author_list.append(commit.author.name)
            committer_list.append(commit.committer.name)
            files_changed_list.append(modification.filename)
            # size_list.append(os.stat(complete_file).st_size)
            lines_added_list.append(commit.insertions)
            lines_removed_list.append(commit.deletions)
        
    raw_data["hash"] = hash_list
    raw_data["date"] = date_list
    raw_data["repo"] = repository_list
    raw_data["author"] = author_list
    raw_data["committer"] = committer_list
    raw_data["files_changed"] = files_changed_list
    # raw_data["size_bytes"] = size_list
    raw_data["lines_added"] = lines_added_list
    raw_data["lines_removed"] = lines_removed_list

    initial_dataframe = pd.DataFrame.from_dict(raw_data, orient="columns")

    return initial_dataframe


def iterate_through_directory(root_directory: str):
    repos_to_check = []
    all_dataframes = []
    final_dataframe = pd.DataFrame()

    for subdir, dirs, files in os.walk(root_directory):
        repos_to_check.append(dirs)
    
    for repository in repos_to_check[0]:
        path = pathlib.Path.home() / root_directory / repository
        initial_dataframe = traverse_all_commits(str(path))
        
        all_dataframes.append(initial_dataframe)
    
    for initial_data in all_dataframes:
        final_dataframe = final_dataframe.append(initial_data)

    
    csv_path = root_directory + "/all_commit_data.csv"

    final_dataframe.to_csv(csv_path)

