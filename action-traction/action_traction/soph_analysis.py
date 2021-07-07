from pydriller import Repository
from nested_lookup import nested_lookup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yaml
import math
import pathlib
import os

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
                file_name_list.append(modification.new_path)
                repository_path_list.append(repository_path)

                source_code_dict["Repository"] = [repository_path]
                source_code_dict["File"] = [modification.new_path]
                source_code_dict["Source Code"] = modification.source_code
                source_code_dict["Date of Commit"] = commit.committer_date
                code_dataframe = pd.DataFrame.from_dict(source_code_dict)
                dataframe_list.append(code_dataframe)
    for result in dataframe_list:
        source_code_dataframe = source_code_dataframe.append(result)
    return source_code_dataframe


def generate_abstract_syntax_trees(source_code_dataframe):
    yaml_list = []
    source_code_list = source_code_dataframe["Source Code"].tolist()
    for source_code in source_code_list:
        if source_code is not None:
            try:
                parsed_yaml = yaml.safe_load(source_code)
                yaml_list.append(parsed_yaml)
            except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
                yaml_list.append("Cannot Parse")
        else:
            yaml_list.append("No file contents")
    source_code_dataframe["Parse Status"] = yaml_list
    yaml_dataframe = source_code_dataframe

    return yaml_dataframe


def find_existing_actions(source_code_dataframe, yaml_dataframe):
    existing_actions_dict = {}
    existing_actions_data = pd.DataFrame()

    # Get necessary information from existing dataframes
    abstract_trees_list = yaml_dataframe["Parse Status"].tolist()
    date_list = source_code_dataframe["Date of Commit"].tolist()
    repository_list = yaml_dataframe["Repository"].tolist()
    file_list = yaml_dataframe["File"].tolist()

    # Iterate abstract syntax trees list and generate list of existing actions for each
    for tree in abstract_trees_list:
        existing_actions = nested_lookup('uses', tree)

    # Create a dictionary with all necessary information
    existing_actions_dict["Date"] = date_list
    existing_actions_dict["Repository"] = repository_list
    existing_actions_dict["File"] = file_list
    existing_actions_dict["Existing Actions Used"] = existing_actions
    existing_actions_dict["Amoung of Existing Actions"] = [len(existing_actions)]

    # Create pandas dataframe from dictionary
    existing_actions_data = pd.DataFrame.from_dict(existing_actions_dict)
    existing_actions_data.set_index('Date', inplace=True)

    return existing_actions_data


def find_user_commands(source_code_dataframe, yaml_dataframe):
    user_commands_dict = {}
    user_commands_data = pd.DataFrame()

    # Get necessary information from existing dataframes
    abstract_trees_list = yaml_dataframe["Parse Status"].tolist()
    date_list = source_code_dataframe["Date of Commit"].tolist()
    repository_list = yaml_dataframe["Repository"].tolist()
    file_list = yaml_dataframe["File"].tolist()

    # Iterate abstract syntax trees list and generate list of defined commands for each
    for tree in abstract_trees_list:
        user_commands = nested_lookup('run', tree)

    # Create a dictionary with all necessary information
    user_commands_dict["Date"] = date_list
    user_commands_dict["Repository"] = repository_list
    user_commands_dict["File"] = file_list
    user_commands_dict["Defined Commands"] = user_commands
    user_commands_dict["Amount of Defined Commands"] = [len(user_commands)]

    # Create pandas dataframe from dictionary
    user_commands_data = pd.DataFrame.from_dict(user_commands_dict)
    user_commands_data.set_index('Date', inplace=True)

    return user_commands_data


def find_os(source_code_dataframe, yaml_dataframe):
    os_dict = {}
    os_data = pd.DataFrame()

    # Get necessary information from existing dataframes
    abstract_trees_list = yaml_dataframe["Parse Status"].tolist()
    date_list = source_code_dataframe["Date of Commit"].tolist()
    repository_list = yaml_dataframe["Repository"].tolist()
    file_list = yaml_dataframe["File"].tolist()

    # Iterate abstract syntax trees list and generate list of operating systems for each
    for tree in abstract_trees_list:
        os = nested_lookup('os', tree)

    # Create a dictionary with all necessary information
    os_dict["Date"] = date_list
    os_dict["Repository"] = repository_list
    os_dict["File"] = file_list
    os_dict["Defined Commands"] = os
    os_dict["Amount of Defined Commands"] = [len(os)]

    # Create pandas dataframe from dictionary
    os_data = pd.DataFrame.from_dict(os_dict)
    os_data.set_index('Date', inplace=True)

    return os_data

def find_envs(source_code_dataframe, yaml_dataframe):
    envs_dict = {}
    envs_data = pd.DataFrame()

    # Get necessary information from existing dataframes
    abstract_trees_list = yaml_dataframe["Parse Status"].tolist()
    date_list = source_code_dataframe["Date of Commit"].tolist()
    repository_list = yaml_dataframe["Repository"].tolist()
    file_list = yaml_dataframe["File"].tolist()

    # Iterate abstract syntax trees list and generate list of existing actions for each
    for tree in abstract_trees_list:
        envs = nested_lookup('run', tree)

    # Create a dictionary with all necessary information
    envs_dict["Date"] = date_list
    envs_dict["Repository"] = repository_list
    envs_dict["File"] = file_list
    envs_dict["Environments Used"] = envs
    envs_dict["Amount of Environments"] = [len(envs)]

    # Create pandas dataframe from dictionary
    envs_data = pd.DataFrame.from_dict(envs_dict)
    envs_data.set_index('Date', inplace=True)

    return envs_data

