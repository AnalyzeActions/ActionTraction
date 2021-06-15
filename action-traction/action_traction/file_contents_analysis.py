from pydriller import Repository
from nested_lookup import nested_lookup
import os
import pathlib
import pandas as pd
import yaml
import re

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
    
    return final_dataframe


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
    
    # yaml_dataframe.to_csv(csv_url)
    return yaml_dataframe

def determine_repositories(initial_data):
    repository_list = initial_data["Repository"].tolist()
    repository_set = set(repository_list)
    return repository_set


def determine_files_per_repo(initial_data, repository_set):
    repo_file_dict = {}
    for repository in repository_set:
        new_data = initial_data.loc[initial_data['Repository'] == repository]
        file_list = new_data["File"].tolist()
        file_set = set(file_list)
        repo_file_dict[repository] = file_set
    return repo_file_dict


def determine_steps_run(yaml_data, repo_file_dict):
    yaml_list = []
    steps_list = []
    steps_run_dict = {}
    dataframe_list = []
    steps_dataframe = pd.DataFrame()
    for repo, file_list in repo_file_dict.items():
        for file in file_list:
            new_data = yaml_data.loc[yaml_data['File'] == file]
            yaml_list = new_data["Parse Status"].tolist()
        
            for parse_tree in yaml_list:
                # print(file)
                steps_run = nested_lookup('uses', parse_tree)
                steps_run_dict["Repository"] = [repo]
                steps_run_dict["File"] = [file]
                steps_run_dict["Step Name"] = [steps_run]
                steps_run_dict["Amount of Steps"] = [len(steps_run)]

                initial_data = pd.DataFrame.from_dict(steps_run_dict)
                dataframe_list.append(initial_data)
    
    for result in dataframe_list:
        steps_dataframe = steps_dataframe.append(result)

    return steps_dataframe
        

def determine_runs(yaml_data, repo_file_dict):
    yaml_list = []
    runs_list = []
    runs_dict = {}
    dataframe_list = []
    runs_dataframe = pd.DataFrame()
    for repo, file_list in repo_file_dict.items():
        for file in file_list:
            new_data = yaml_data.loc[yaml_data['File'] == file]
            yaml_list = new_data["Parse Status"].tolist()
        
            for parse_tree in yaml_list:
                # print(file)
                defined_command = nested_lookup('run', parse_tree)
                runs_dict["Repository"] = [repo]
                runs_dict["File"] = [file]
                runs_dict["Run Command"] = [defined_command]
                runs_dict["Amount of Defined Commands"] = [len(defined_command)]

                initial_data = pd.DataFrame.from_dict(runs_dict)
                dataframe_list.append(initial_data)
    
    for result in dataframe_list:
        runs_dataframe = runs_dataframe.append(result)

    return runs_dataframe


def determine_operating_systems(yaml_data, repo_file_dict):
    yaml_list = []
    operating_systems_list = []
    operating_systems_dict = {}
    dataframe_list = []
    operating_systems_dataframe = pd.DataFrame()
    for repo, file_list in repo_file_dict.items():
        for file in file_list:
            new_data = yaml_data.loc[yaml_data['File'] == file]
            yaml_list = new_data["Parse Status"].tolist()
        
            for parse_tree in yaml_list:
                # print(file)
                defined_os = nested_lookup('os', parse_tree)
                operating_systems_dict["Repository"] = [repo]
                operating_systems_dict["File"] = [file]
                operating_systems_dict["Operating Systems Used"] = [defined_os]
                operating_systems_dict["Amount of Operating Systems"] = [len(defined_os)]

                initial_data = pd.DataFrame.from_dict(operating_systems_dict)
                dataframe_list.append(initial_data)
    
    for result in dataframe_list:
        operating_systems_dataframe = operating_systems_dataframe.append(result)

    # print(operating_systems_dataframe)
    return operating_systems_dataframe


def determine_environments(yaml_data, repo_file_dict):
    yaml_list = []
    environments_list = []
    environments_dict = {}
    dataframe_list = []
    environments_dataframe = pd.DataFrame()
    for repo, file_list in repo_file_dict.items():
        for file in file_list:
            new_data = yaml_data.loc[yaml_data['File'] == file]
            yaml_list = new_data["Parse Status"].tolist()
        
            for parse_tree in yaml_list:
                # print(file)
                defined_environments = nested_lookup('os', parse_tree)
                environments_dict["Repository"] = [repo]
                environments_dict["File"] = [file]
                environments_dict["Environments Used"] = [defined_environments]
                environments_dict["Amount of Environments Systems"] = [len(defined_environments)]

                initial_data = pd.DataFrame.from_dict(environments_dict)
                dataframe_list.append(initial_data)
    
    for result in dataframe_list:
        environments_dataframe = environments_dataframe.append(result)

    # print(operating_systems_dataframe)
    return environments_dataframe


def determine_languages(yaml_data, repo_file_dict):
    yaml_list = []
    languages_list = []
    languages_dict = {}
    dataframe_list = []
    regex = re.compile("\w+(?:-version)")
    languages_dataframe = pd.DataFrame()
    for repo, file_list in repo_file_dict.items():
        for file in file_list:
            new_data = yaml_data.loc[yaml_data['File'] == file]
            yaml_list = new_data["Parse Status"].tolist()
        
            for parse_tree in yaml_list:
                # print(file)
                defined_languages = nested_lookup(regex, parse_tree)
                print(defined_languages)
                languages_dict["Repository"] = [repo]
                languages_dict["File"] = [file]
                languages_dict["Environments Used"] = [defined_languages]
                languages_dict["Amount of Environments Systems"] = [len(defined_languages)]

                initial_data = pd.DataFrame.from_dict(languages_dict)
                dataframe_list.append(initial_data)
    
    for result in dataframe_list:
        languages_dataframe = languages_dataframe.append(result)

    # print(operating_systems_dataframe)
    return languages_dataframe



def popularity_helper(specified_data, identifier):
    repo_metrics = []
    all_metrics = []
    repo_count = 0
    popularity_dict = {}
    metric_names = []
    amount_repos = []
    percentage_list = []
    # Generate set of repositories
    total_repositories = specified_data['Repository'].tolist()
    individual_repos = set(total_repositories)
    for repo in individual_repos:
        new_data = specified_data.loc[specified_data['Repository'] == repo]
        identifier_list = new_data[identifier].tolist()
        if identifier_list is not None:
            repo_count = repo_count + 1
        repo_set = {}
        for multiple_items in identifier_list:
            for item in multiple_items:
                repo_metrics.append(item)
                repo_set = set(repo_metrics)
        for metric in repo_set:
            all_metrics.append(metric)
        
    final_set = set(all_metrics)
    for individual_metric in all_metrics:
        popularity_dict[individual_metric] = all_metrics.count(individual_metric)

    return popularity_dict


def determine_steps_popularity(steps_dataframe):
    popular_steps = popularity_helper("Step Name")
    return popular_steps


def determine_runs_popularity(runs_dataframe):
    popular_runs = popularity_helper("Run Command")
    return popular_runs


def understand_steps_lifetime(steps_dataframe, repository):
    print(steps_dataframe["Date of Commit"])


# def understand_runs_lifetime(runs_dataframe, repository):

# def compare_steps_and_runs(runs_dataframe, steps_dataframe, repo_file_dict):
#     runs_repositories = runs_dataframe['Repository'].tolist()
#     runs_repos = set(runs_repositories)
#     steps_repositories = steps_dataframe['Repository'].tolist()
#     steps_repos = set(steps_repositories)
#     total_runs = {}
#     total_steps = {}
#     comparison_dict = {}
#     for repo in runs_repos:
#         runs_data = runs_dataframe.loc[runs_dataframe['Repository'] == repo]
#         amount_of_runs = runs_data["Amount of Defined Commands"].tolist()
#         total_runs[repo] = amount_of_runs[len(amount_of_runs) - 1]
#     for repo in steps_repos:
#         steps_data = steps_dataframe.loc[steps_dataframe['Repository'] == repo]
#         amount_of_steps = steps_dataframe["Amount of Steps"].tolist()
#         total_steps[repo] = amount_of_steps[len(amount_of_steps) - 1]











def perform_specified_analysis(directory, specified_metrics):
    source_code_data = iterate_through_directory(directory)
    repo_set = determine_repositories(source_code_data)
    repo_file_dict = determine_files_per_repo(source_code_data, repo_set)
    yaml_data = generate_abstract_syntax_trees(source_code_data)

    if "Actions" in specified_metrics:
        steps_dataframe = determine_steps_run(yaml_data, repo_file_dict)
        popular_steps = determine_steps_popularity(steps_dataframe)
        print(steps_dataframe)
        print(popular_steps)
    if "Commands" in specified_metrics:
        commands_dataframe = determine_runs(yaml_data, repo_file_dict)
        popular_commands = determine_runs_popularity(commands_dataframe)
        print(commands_dataframe)
        print(popular_commands)
    # if "Comparison" in specified_metrics:
    #     steps_dataframe = determine_steps_run(yaml_data, repo_file_dict)
    #     commands_dataframe = determine_runs(yaml_daata, repo_file_dict)
    #     comparison = compare_steps_and_runs(steps_dataframe, commands_dataframe)
    #     print(comparison)
    # if "Lifetime" in specified_metrics:
    if "Setup" in specified_metrics:
        operating_systems = determine_operating_systems(yaml_data, repo_file_dict)
        environments = determine_environments(yaml_data, repo_file_dict)
        determine_languages(yaml_data, repo_file_dict)
        # print(operating_systems)
        # print(environments)
        # print(languages)


# Number Nodes/Edges (AST Size)
# Number jobs / runs
# Types of jobs / runs (names)
# Languages
# Contents of each step
# How many environment variables (env)
# Jobs (steps) vs runs
# Job / Run popularity