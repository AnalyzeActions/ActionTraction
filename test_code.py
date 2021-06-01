from pydriller import RepositoryMining



import pandas as pd
import numpy as np
import os

#TODO: Function to combine for list of functions (create pd dataframe)

def generate_file_list(repository_path: str):
    files_changed_list = []
    for commit in RepositoryMining(repository_path, only_modifications_with_file_types=['.yml']).traverse_commits():
        for modified_file in commit.modifications:
            if modified_file != None:
                files_changed_list.append(modified_file._new_path)
    
    print(files_changed_list)
        


if __name__ == "__main__":
    # files_changed = generate_file_list("/home/mkapfhammer/Documents/predictiveWellness")
    # actions_files = determine_actions_files(files_changed)
    # data = iterate_actions_files("/home/mkapfhammer/Documents/predictiveWellness", actions_files)
    # print(data)
    # iterate_through_directory("/home/mkapfhammer/Documents")
    generate_file_list("/home/mkapfhammer/Documents/test_traction/predictiveWellness")