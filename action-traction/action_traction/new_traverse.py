from pydriller import Repository
import pandas as pd
import os
import pathlib
from ordered_set import OrderedSet

from action_traction import constants
from rich.console import Console
from rich.progress import BarColumn
from rich.progress import Progress
from rich.progress import TimeRemainingColumn
from rich.progress import TimeElapsedColumn

def traverse_all_commits(repository_path: str):
    """Traverse all commits of a repository and create a dataframe with all important information."""
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

            p = pathlib.Path(repository_path)
            p.mkdir(parents=True, exist_ok=True)
            fn = "size.yml"
            file_path = p / fn
            with file_path.open("w", encoding = "utf-8") as f:
                if modification.source_code is not None:
                    f.write(modification.source_code)
                else:
                    f.write("")
            
            complete_file = repository_path + "/size.yml"
            # print(complete_file)

            hash_list.append(commit.hash)
            date_list.append(commit.committer_date)
            repository_list.append(repository_path)
            author_list.append(commit.author.name)
            committer_list.append(commit.committer.name)
            files_changed_list.append(modification.new_path)
            size_list.append(os.stat(complete_file).st_size)
            lines_added_list.append(commit.insertions)
            lines_removed_list.append(commit.deletions)
            source_code_list.append(modification.source_code)
        
    raw_data["hash"] = hash_list
    raw_data["date"] = date_list
    raw_data["repo"] = repository_list
    raw_data["author"] = author_list
    raw_data["committer"] = committer_list
    raw_data["file_changed"] = files_changed_list
    raw_data["size_bytes"] = size_list
    raw_data["lines_added"] = lines_added_list
    raw_data["lines_removed"] = lines_removed_list
    raw_data["source_code"] = source_code_list

    initial_dataframe = pd.DataFrame.from_dict(raw_data, orient="columns")

    return initial_dataframe


def create_intermediate_dataframe(all_commits_dataframe):
    """Create a dataframe to indicate whether GitHub actions were changed for each commit."""
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
        files_changed_list = raw_data["file_changed"].tolist()
        
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

    intermediate_data = pd.DataFrame.from_dict(intermediate_dict)

    return intermediate_data


def start_at_gha_dataframe(intermediate_data):
    """Pair down beginning dataframe to only include commits after gha were introduced."""
    gha_data = intermediate_data.loc[intermediate_data["gha_present"] == True]
    gha_data.reset_index(drop=True)
    return gha_data


def populate_smaller_dataset(gha_data, all_commit_data):
    """Populate a dataset with all information relating to gha changed, and commits where gha was not changed."""
    count = 0
    gha_files = []
    all_files_changed = all_commit_data["file_changed"].tolist()
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
        
    return final_data
    

def join_dataframes(gha_data, final_data):
    """Merge dataframes to add True/False of if GitHub Actions were changed."""
    merged = pd.merge(gha_data, final_data, how="right", on=["hash"])

    return merged


def iterate_through_directory(root_directory: str):
    """Iterate through the given directory and create all necessary datasets."""
    repos_to_check = []
    all_dataframes = []
    all_commit_data = pd.DataFrame()

    for subdir, dirs, files in os.walk(root_directory):
        repos_to_check.append(dirs)
    

    with Progress(
        constants.progress.Task_Format,
        BarColumn(),
        constants.progress.Percentage_Format,
        constants.progress.Completed,
        "•",
        TimeElapsedColumn(),
        "elapsed",
        "•",
        TimeRemainingColumn(),
        "remaining",
    ) as progress:
        generate_metrics = progress.add_task("Generating Repository Metrics", total=len(repos_to_check[0]))
        for repository in repos_to_check[0]:
            path = pathlib.Path.home() / root_directory / repository
            initial_dataframe = traverse_all_commits(str(path))
            
            all_dataframes.append(initial_dataframe)
            progress.update(generate_metrics, advance=1)
    
    for initial_data in all_dataframes:
        all_commit_data = all_commit_data.append(initial_data)


    intermediate_dataframe = create_intermediate_dataframe(all_commit_data)

    gha_dataframe = start_at_gha_dataframe(intermediate_dataframe)

    final_dataset = populate_smaller_dataset(gha_dataframe, all_commit_data)

    merged_dataset = join_dataframes(gha_dataframe, final_dataset)

    # Put all dataframes into .csv files
    all_commit_data.to_csv(root_directory + "/all_commit_data.csv")
    gha_dataframe.to_csv(root_directory + "/beginning_github_actions.csv")
    merged_dataset.to_csv(root_directory + "/final_data.csv")
