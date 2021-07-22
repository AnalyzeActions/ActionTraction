from pydriller import Repository
import pandas as pd
import os
import pathlib
from ordered_set import OrderedSet

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
    source_code_list = []

    raw_data = {}

    for commit in Repository(repository_path).traverse_commits():
        for modification in commit.modified_files:
            complete_file = repository_path + "/" + modification.filename

            hash_list.append(commit.hash)
            date_list.append(commit.committer_date)
            repository_list.append(repository_path)
            author_list.append(commit.author.name)
            committer_list.append(commit.committer.name)
            files_changed_list.append(modification.new_path)
            # size_list.append(os.stat(complete_file).st_size)
            lines_added_list.append(commit.insertions)
            lines_removed_list.append(commit.deletions)
            source_code_list.append(modification.source_code)
        
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


def create_intermediate_dataframe(all_commit_csv: str):
    all_commits_dataframe = pd.read_csv(all_commit_csv)

    hash_list = all_commits_dataframe["hash"].tolist()
    hash_set = OrderedSet(hash_list)

    intermediate_dict = {}
    yes_gha = []
    hash_list = []
    gha_list = []
    present_list = []

    present = False

    for unique_hash in hash_set:
        raw_data = all_commits_dataframe.loc[all_commits_dataframe["hash"] == unique_hash]
        files_changed_list = raw_data["files_changed"].tolist()
        
        hash_list.append(unique_hash)

        
        if any(".github/workflows" in str(file) for file in files_changed_list):
            gha_list.append(True)
            present = True
        else:
            gha_list.append(False)
        
        if present:
            present_list.append(present)
        else:
            present_list.append(False)
        
    intermediate_dict["hash"] = hash_list
    intermediate_dict["gha_changed"] = gha_list
    intermediate_dict["gha_present"] = present_list

    # print(len(hash_list))
    # print(len(gha_list))

    # print(intermediate_dict)
    intermediate_data = pd.DataFrame.from_dict(intermediate_dict)
    # intermediate_data.set_index("hash", inplace=True)
    return intermediate_data


def start_at_gha_dataframe(intermediate_data):
    gha_data_start = intermediate_data.loc[intermediate_data["gha_present"] == True]
    gha_data_start.to_csv("/home/mkapfhammer/Documents/try_faker/gha_data.csv", index=False)
    gha_data_start.reset_index(drop=True)
    return gha_data_start


def populate_smaller_dataset(gha_data, all_commit_data):
    count = 0
    gha_files = []
    all_files_changed = all_commit_data["files_changed"].tolist()
    all_files_set = OrderedSet(all_files_changed)
    initial_data_list = []
    hash_list = []
    secondary_data = pd.DataFrame()
    final_data = pd.DataFrame()

    for index, row in gha_data.iterrows():
        changed = row["gha_changed"]
        if changed == True:
            unique_hash = row["hash"]
            secondary_data = all_commit_data.loc[all_commit_data["hash"] == unique_hash]
            initial_data_list.append(secondary_data)
        elif changed == False:
            correct_hash = row["hash"]
            raw_data = initial_data_list[len(initial_data_list)-1]
            changed_data = raw_data.copy(deep=True)
            
            changed_data["hash"] = correct_hash

            # raw_data["hash"] = hash_list
            initial_data_list.append(changed_data)
            
    for dataframe in initial_data_list:
        final_data = final_data.append(dataframe)
    
    final_data.to_csv("/home/mkapfhammer/Documents/try_faker/secondary.csv")

    