from pydriller import Repository
from nested_lookup import nested_lookup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yaml
import math
import pathlib
import os
import statistics

def generate_file_list(repository_path: str):
    files_changed_list = []
    for commit in Repository(repository_path, only_modifications_with_file_types=['.yml']).traverse_commits():
        for changed_file in commit.modified_files:
            files_changed_list.append(changed_file.new_path)
    
    return files_changed_list


def determine_actions_files(modified_files: List[str]):
    files_to_analyze = []
    for file in modified_files:
        if ".github" in str(file):
            if files_to_analyze.count(str(file)) == 0:
                files_to_analyze.append(str(file))
    
    return files_to_analyze


def generate_size_data(repository_path, files_to_analyze):
    raw_data = {}
    repository_list = []
    file_list = []
    size_list = []
    date_list = []

    # Traverse repository and gather all information relating to file size
    for file in files_to_analyze:
        for commit in Repository(repository_path, filepath=file).traverse_commits():
            complete_file = repository_path + "/" + file
            repository_list.append(file)
            file_list.append(file)
            size_list.append(os.stat(complete_file).st_size)
            date_list.append(commit.committer_date)

    # Create raw dictionary with information relating to file size
    raw_data["Date"] = date_list
    raw_data["Repository"] = repository_list
    raw_data["File"] = file_list
    raw_data["File Size in Bytes"] = date_list

    return raw_data


def generate_author_data(repository_path, files_to_analyze):
    raw_data = {}
    repository_list = []
    file_list = []
    author_list = []
    date_list = []

    # Traverse repository and gather all information relating to commit authors
    for file in files_to_analyze:
        for commit in Repository(repository_path, filepath=file).traverse_commits():
            complete_file = repository_path + "/" + file
            repository_list.append(file)
            file_list.append(file)
            author_list.append(commit.author.name)
            date_list.append(commit.committer_date)

    # Create raw dictionary with information relating to commit authors
    raw_data["Date"] = date_list
    raw_data["Repository"] = repository_list
    raw_data["File"] = file_list
    raw_data["Author"] = author_list

    return raw_data


def generate_committer_data(repository_path, files_to_analyze):
    raw_data = {}
    repository_list = []
    file_list = []
    committer_list = []
    date_list = []

    # Traverse repository and gather all information relating to committers
    for file in files_to_analyze:
        for commit in Repository(repository_path, filepath=file).traverse_commits():
            complete_file = repository_path + "/" + file
            repository_list.append(file)
            file_list.append(file)
            committer_list.append(commit.committer.name)
            date_list.append(commit.committer_date)

    # Create raw dictionary with information relating to committers
    raw_data["Date"] = date_list
    raw_data["Repository"] = repository_list
    raw_data["File"] = file_list
    raw_data["Committer"] = committer_list

    return raw_data


def generate_lines_added_data(repository_path, files_to_analyze):
    raw_data = {}
    repository_list = []
    file_list = []
    lines_added_list = []
    date_list = []

    # Traverse repository and gather all information relating to lines added
    for file in files_to_analyze:
        for commit in Repository(repository_path, filepath=file).traverse_commits():
            complete_file = repository_path + "/" + file
            repository_list.append(file)
            file_list.append(file)
            lines_added_list.append(commit.insertions)
            date_list.append(commit.committer_date)

    # Create raw dictionary with information relating to lines added
    raw_data["Date"] = date_list
    raw_data["Repository"] = repository_list
    raw_data["File"] = file_list
    raw_data["Lines Added"] = lines_added_list

    return raw_data


def generate_lines_removed_data(repository_path, files_to_analyze):
    raw_data = {}
    repository_list = []
    file_list = []
    lines_removed_list = []
    date_list = []

    # Traverse repository and gather all information relating to lines removed
    for file in files_to_analyze:
        for commit in Repository(repository_path, filepath=file).traverse_commits():
            complete_file = repository_path + "/" + file
            repository_list.append(file)
            file_list.append(file)
            lines_removed_list.append(commit.deletions)
            date_list.append(commit.committer_date)

    # Create raw dictionary with information relating to lines removed
    raw_data["Date"] = date_list
    raw_data["Repository"] = repository_list
    raw_data["File"] = file_list
    raw_data["Lines Removed"] = lines_removed_list

    return raw_data


def perform_calculations(data, specified_category):
    specific_list = data[specified_category]
    # Determine minimum of metric
    minimum = min(specific_list)
    # Determine maximum of metric
    maximum = max(specific_list)
    # Determine mean of metric
    mean = statistics.mean(specific_list)
    # Determine median of metric
    median = statistics.median(specific_list)
    # Determine standard deviation of metric
    st_dev = statistics.stdev(specific_list)
    # Determine variance of metric 
    variance = statistics.variance(specific_list)

    return minimum, maximum, mean, median, st_dev, variance












