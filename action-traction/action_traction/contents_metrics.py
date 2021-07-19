"""A program to determine the contents of GitHub Actions configuration files over time."""
from pydriller import Repository
from nested_lookup import nested_lookup
import os
import pathlib
import pandas as pd
import yaml
import re


def determine_file_contents(repository_path: str):
    """Traverse a GitHub Repository and gather source code."""
    actions_files = []
    source_code_dict = {}
    dataframe_list = []
    file_name_list = []
    repository_path_list = []
    source_code_dataframe = pd.DataFrame()

    # Iterate through repository commits
    for commit in Repository(repository_path).traverse_commits():
        for modification in commit.modified_files:
            # Only gather information for GitHub Actions configurations
            if ".github" in str(modification.new_path):
                actions_files.append(modification.source_code)
                file_name_list.append(modification.new_path)
                repository_path_list.append(repository_path)

                # Create a dictionary of all repo information and its source code
                source_code_dict["repo"] = [repository_path]
                source_code_dict["file"] = [modification.new_path]
                source_code_dict["source_code"] = modification.source_code
                source_code_dict["date"] = commit.committer_date
                code_dataframe = pd.DataFrame.from_dict(source_code_dict)
                dataframe_list.append(code_dataframe)

    for result in dataframe_list:
        source_code_dataframe = source_code_dataframe.append(result)

    return source_code_dataframe


def iterate_through_directory(root_directory: str):
    """Iterate through a directory and determine the repositories that are in it."""
    repos_to_check = []
    dataframes_list = []
    final_dataframe = pd.DataFrame()

    # Iterate through directory and determine repositories
    for subdir, dirs, files in os.walk(root_directory):
        repos_to_check.append(dirs)

    for repository in repos_to_check[0]:
        # Create complete paths for each repository
        path = pathlib.Path.home() / root_directory / repository
        # Create a dataframe for each repository in a directory
        source_code_dataframe = determine_file_contents(str(path))
        dataframes_list.append(source_code_dataframe)

    for initial_data in dataframes_list:
        final_dataframe = final_dataframe.append(initial_data)

    return final_dataframe


def generate_abstract_syntax_trees(source_code_dataframe):
    """Generate the abstract syntax trees of GitHub Actions configurations source code."""
    yaml_list = []
    source_code_list = source_code_dataframe["source_code"].tolist()
    for source_code in source_code_list:
        if source_code is not None:
            try:
                parsed_yaml = yaml.safe_load(source_code)
                yaml_list.append(parsed_yaml)
            except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
                yaml_list.append("Cannot Parse")
        else:
            yaml_list.append("No file contents")
    source_code_dataframe["parse_status"] = yaml_list
    yaml_dataframe = source_code_dataframe

    return yaml_dataframe


def determine_repositories(initial_data):
    """Create a set of the unique repositories in a dataframe."""
    repository_list = initial_data["Repository"].tolist()
    repository_set = set(repository_list)
    return repository_set


def determine_files_per_repo(initial_data, repository_set):
    """Determine the GitHub Actions files for each repository."""
    repo_file_dict = {}
    for repository in repository_set:
        new_data = initial_data.loc[initial_data["repo"] == repository]
        file_list = new_data["file"].tolist()
        file_set = set(file_list)
        repo_file_dict[repository] = file_set
    return repo_file_dict


def determine_steps_run(yaml_data, repo_file_dict):
    """Determine the defined GitHub Actions used in a configuration file."""
    yaml_list = []
    steps_run_dict = {}
    dataframe_list = []
    steps_dataframe = pd.DataFrame()
    for repo, file_list in repo_file_dict.items():
        for file in file_list:
            new_data = yaml_data.loc[yaml_data["file"] == file]
            yaml_list = new_data["parse_status"].tolist()

            for parse_tree in yaml_list:
                steps_run = nested_lookup("uses", parse_tree)
                steps_run_dict["repo"] = [repo]
                steps_run_dict["file"] = [file]
                steps_run_dict["defined_action"] = [steps_run]
                steps_run_dict["amount_actions"] = [len(steps_run)]

                initial_data = pd.DataFrame.from_dict(steps_run_dict)
                dataframe_list.append(initial_data)

    for result in dataframe_list:
        steps_dataframe = steps_dataframe.append(result)

    return steps_dataframe


def determine_runs(yaml_data, repo_file_dict):
    """Determine the specified commands run in a GitHub Actions configuration file."""
    yaml_list = []
    runs_dict = {}
    dataframe_list = []
    runs_dataframe = pd.DataFrame()
    for repo, file_list in repo_file_dict.items():
        for file in file_list:
            new_data = yaml_data.loc[yaml_data["file"] == file]
            yaml_list = new_data["parse_status"].tolist()

            for parse_tree in yaml_list:
                defined_command = nested_lookup("run", parse_tree)
                runs_dict["repo"] = [repo]
                runs_dict["file"] = [file]
                runs_dict["specified_command"] = [defined_command]
                runs_dict["amount_commands"] = [len(defined_command)]

                initial_data = pd.DataFrame.from_dict(runs_dict)
                dataframe_list.append(initial_data)

    for result in dataframe_list:
        runs_dataframe = runs_dataframe.append(result)

    return runs_dataframe


def determine_operating_systems(yaml_data, repo_file_dict):
    """Determine operating systems used in a GitHub Action configuration file."""
    yaml_list = []
    operating_systems_dict = {}
    dataframe_list = []
    operating_systems_dataframe = pd.DataFrame()
    for repo, file_list in repo_file_dict.items():
        for file in file_list:
            new_data = yaml_data.loc[yaml_data["file"] == file]
            yaml_list = new_data["parse_status"].tolist()

            for parse_tree in yaml_list:
                defined_os = nested_lookup("os", parse_tree)
                operating_systems_dict["repo"] = [repo]
                operating_systems_dict["file"] = [file]
                operating_systems_dict["operating_systems"] = [defined_os]
                operating_systems_dict["amount_os"] = [
                    len(defined_os)
                ]

                initial_data = pd.DataFrame.from_dict(operating_systems_dict)
                dataframe_list.append(initial_data)

    for result in dataframe_list:
        operating_systems_dataframe = operating_systems_dataframe.append(result)

    return operating_systems_dataframe


def determine_environments(yaml_data, repo_file_dict):
    """Determine the environments used in a GitHub Action configuration file."""
    yaml_list = []
    environments_dict = {}
    dataframe_list = []
    environments_dataframe = pd.DataFrame()
    for repo, file_list in repo_file_dict.items():
        for file in file_list:
            new_data = yaml_data.loc[yaml_data["file"] == file]
            yaml_list = new_data["parse_status"].tolist()

            for parse_tree in yaml_list:
                defined_environments = nested_lookup("env", parse_tree)
                environments_dict["repo"] = [repo]
                environments_dict["file"] = [file]
                environments_dict["environments"] = [defined_environments]
                environments_dict["amount_envs"] = [
                    len(defined_environments)
                ]

                initial_data = pd.DataFrame.from_dict(environments_dict)
                dataframe_list.append(initial_data)

    for result in dataframe_list:
        environments_dataframe = environments_dataframe.append(result)

    return environments_dataframe


def determine_languages(yaml_data, repo_file_dict):
    """Determine the programming languages used in a GitHub Action configuration file."""
    yaml_list = []
    languages_dict = {}
    dataframe_list = []
    regex = re.compile(r"\w+(?:-version)")
    languages_dataframe = pd.DataFrame()
    for repo, file_list in repo_file_dict.items():
        for file in file_list:
            new_data = yaml_data.loc[yaml_data["file"] == file]
            yaml_list = new_data["parse_status"].tolist()

            for parse_tree in yaml_list:
                defined_languages = nested_lookup(regex, parse_tree)
                print(defined_languages)
                languages_dict["repo"] = [repo]
                languages_dict["file"] = [file]
                languages_dict["languages"] = [defined_languages]
                languages_dict["amount_languages"] = [len(defined_languages)]

                initial_data = pd.DataFrame.from_dict(languages_dict)
                dataframe_list.append(initial_data)

    for result in dataframe_list:
        languages_dataframe = languages_dataframe.append(result)

    return languages_dataframe


def popularity_helper(specified_data, identifier):
    """Determine the popularity of a specific metric."""
    repo_metrics = []
    all_metrics = []
    repo_count = 0
    popularity_dict = {}
    # Generate set of repositories
    total_repositories = specified_data["repo"].tolist()
    individual_repos = set(total_repositories)
    for repo in individual_repos:
        new_data = specified_data.loc[specified_data["repo"] == repo]
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

    for individual_metric in all_metrics:
        popularity_dict[individual_metric] = all_metrics.count(individual_metric)

    return popularity_dict


def determine_steps_popularity(steps_dataframe):
    """Determine popularity of defined GitHub Actions."""
    popular_steps = popularity_helper(steps_dataframe, "defined_action")
    return popular_steps


def determine_runs_popularity(runs_dataframe):
    """Determine popularity of specified commands."""
    popular_runs = popularity_helper(runs_dataframe, "specified_command")
    return popular_runs


def contents_over_time(directory):
    """Determine the contents of a GitHub Action configuration file over time."""
    complete_dataframe = pd.DataFrame()
    steps_list = []
    commands_list = []
    commands_amount_list = []
    os_list = []
    os_amount_list = []
    env_list = []
    env_amount_list = []

    source_code_data = iterate_through_directory(directory)
    repo_set = determine_repositories(source_code_data)
    repo_file_dict = determine_files_per_repo(source_code_data, repo_set)
    yaml_data = generate_abstract_syntax_trees(source_code_data)

    steps_dataframe = determine_steps_run(yaml_data, repo_file_dict)
    commands_dataframe = determine_runs(yaml_data, repo_file_dict)
    operating_systems = determine_operating_systems(yaml_data, repo_file_dict)
    environments = determine_environments(yaml_data, repo_file_dict)
    # languages = determine_languages(yaml_data, repo_file_dict) # Regular expression not currently working

    complete_dataframe = steps_dataframe
    steps_list = steps_dataframe["defined_action"].tolist()
    step_amount_list = steps_dataframe["amount_actions"].tolist()
    commands_list = commands_dataframe["specified_command"].tolist()
    commands_amount_list = commands_dataframe["amount_commands"].tolist()
    os_list = operating_systems["operating_systems"].tolist()
    os_amount_list = operating_systems["amount_os"].tolist()
    env_list = environments["environments"].tolist()
    env_amount_list = environments["amount_envs"]

    complete_dataframe["defined_action"] = steps_list
    complete_dataframe["amount_action"] = step_amount_list
    complete_dataframe["specified_command"] = commands_list
    complete_dataframe["amount_commands"] = commands_amount_list
    complete_dataframe["operating_systems"] = os_list
    complete_dataframe["amount_os"] = os_amount_list
    complete_dataframe["environments"] = env_list
    complete_dataframe["amount_envs"] = env_amount_list

    complete_dataframe_path = directory + "/fileContentsAnalysis.csv"
    complete_dataframe.to_csv(complete_dataframe_path)
    return complete_dataframe
