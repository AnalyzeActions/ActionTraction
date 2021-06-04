from pydriller import Repository
import os
import pathlib
import pandas as pd

def determine_file_contents(repository_path: str):
    actions_files = []
    source_code_dict = {}
    dataframe_list = []
    file_name_list = []
    repository_path_list = []
    source_code_dataframe = pd.DataFrame()
    for commit in Repository(repository_path).traverse_commits():
        for modification in commit.modified_files:
            if ".github" in str(modification.new_path):
                actions_files.append(modification.source_code)
                # print(modification.new_path)
                file_name_list.append(modification.new_path)
                repository_path_list.append(repository_path)

    # print(len(file_name_list))
    # print(len(repository_path))
    # print(len(actions_files))
                source_code_dict["Repository"] = [repository_path]
                source_code_dict["File"] = [modification.new_path]
                source_code_dict["Source Code"] = modification.source_code
                code_dataframe = pd.DataFrame.from_dict(source_code_dict)
                dataframe_list.append(code_dataframe)
    for result in dataframe_list:
        source_code_dataframe = source_code_dataframe.append(result)
    return source_code_dataframe
    # print(source_code_dict)


def iterate_through_directory(root_directory: str):
    repos_to_check = []
    dataframes_list = []
    final_dataframe = pd.DataFrame()
    for subdir, dirs, files in os.walk(root_directory):
        repos_to_check.append(dirs)
    
    for repository in repos_to_check[0]:
        path = pathlib.Path.home() / root_directory / repository
        source_code_dataframe = determine_file_contents(str(path))
        dataframes_list.append(source_code_dataframe)
    
    for initial_data in dataframes_list:
        final_dataframe = final_dataframe.append(initial_data)
    
    print(final_dataframe)