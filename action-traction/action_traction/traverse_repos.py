# from pydriller import RepositoryMining
from pydriller import Repository
import pandas as pd


def generate_file_list(repository_path):
    files_changed_list = []
    for commit in Repository(repository_path, only_modifications_with_file_types=['.yml']).traverse_commits():
        for modified_file in commit.modifications:
            if modified_file != None:
                files_changed_list.append(modified_file._new_path)
    
    return files_changed_list


def determine_actions_files(modified_files):
    files_to_analyze = []
    for file_list in modified_files:
        for file in file_list:
            if ".github" in str(file):
                if files_to_analyze.count(str(file)) == 0:
                    files_to_analyze.append(str(file))
    
    return files_to_analyze


def iterate_actions_files(repository_path, files_to_analyze):
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
    
    return author_list
