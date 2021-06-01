# from pydriller import RepositoryMining
from pydriller import Repository
from typing import List
import pandas as pd
import numpy as np
import os
import pathlib

#TODO: Function to combine for list of functions (create pd dataframe)

def generate_file_list(repository_path: str):
    files_changed_list = []
    for commit in Repository(repository_path, only_modifications_with_file_types=['.yml']).traverse_commits():
        for modified_file in commit.modifications:
            if modified_file != None:
                files_changed_list.append(modified_file._new_path)
    
    return files_changed_list


def determine_actions_files(modified_files: List[str]):
    files_to_analyze = []
    for file_list in modified_files:
        for file in file_list:
            if ".github" in str(file):
                if files_to_analyze.count(str(file)) == 0:
                    files_to_analyze.append(str(file))
    
    return files_to_analyze


def iterate_actions_files(repository_path: str, files_to_analyze: List[str]):
    author_list = []
    committer_list = []
    date_list = []
    branches_list = []
    commit_messages_list = []
    files_changed_list = []
    lines_added_list = []
    lines_deleted_list = []
    source_code_list = []
    lines_of_code_list = []
    for file in files_to_analyze:
        for commit in Repository(repository_path, filepath=file).traverse_commits(): 
            author_list.append(commit.author.name)
            committer_list.append(commit.committer.name)
            date_list.append(commit.committer_date) #TODO: Format date
            branches_list.append(commit.branches)
            commit_messages_list.append(commit.msg)
            for modification in commit.modifications:
                source_code_list.append(str(modification.source_code))
                lines_added_list.append(modification.added)
                lines_deleted_list.append(modification.deleted)
                lines_of_code_list.append(modification.nloc)
    
    dataframe = pd.DataFrame(np.array(([author_list, committer_list]), columns=['Authors', 'Committers']))
    return dataframe


def iterate_through_directory(root_directory: str):
    repos_to_check = []
    for subdir, dirs, files in os.walk(root_directory):
        repos_to_check.append(dirs)
    
    for repository in repos_to_check[0]:
        path = pathlib.Path.home() / root_directory / repository
        all_files_changed = generate_file_list(str(path))
        actions_files = determine_actions_files(all_files_changed)
        dataframe = iterate_actions_files

    return dataframe
# def iterate_through_paths(path_list):


#TODO: Type annotate functions
