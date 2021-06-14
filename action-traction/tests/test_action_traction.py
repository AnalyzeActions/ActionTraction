from action_traction import __version__
from action_traction import download_repos
from action_traction import traverse_repos
from action_traction import basic_analysis_calculations as basic
import os
import pandas as pd

def test_version():
    assert __version__ == '0.1.0'

def test_generate_paths():
    repository_list = ["Repo_one", "Repo_two", "Repo_three"]
    directory = "/home/mkapfhammer/Documents"
    path_list = download_repos.generate_save_path(repository_list, directory)
    assert len(path_list) == 3


def test_calculate_size_metrics():
    test_dictionary = {}
    test_dictionary["File Size in Bytes"] = [455, 327, 80, 540]
    test_data = pd.DataFrame.from_dict(test_dictionary, orient="columns")
    size_dictionary = basic.calculate_size_metrics(test_data)
    assert len(size_dictionary) == 4

def test_size_minimum():
    test_dictionary = {}
    test_dictionary["File Size in Bytes"] = [455, 327, 80, 540]
    test_data = pd.DataFrame.from_dict(test_dictionary, orient="columns")
    size_dictionary = basic.calculate_size_metrics(test_data)
    assert size_dictionary["Minimum"] == 80


def test_size_maximum():
    test_dictionary = {}
    test_dictionary["File Size in Bytes"] = [455, 327, 80, 540]
    test_data = pd.DataFrame.from_dict(test_dictionary, orient="columns")
    size_dictionary = basic.calculate_size_metrics(test_data)
    assert size_dictionary["Maximum"] == 540


def test_size_mean():
    test_dictionary = {}
    test_dictionary["File Size in Bytes"] = [455, 327, 80, 540]
    test_data = pd.DataFrame.from_dict(test_dictionary, orient="columns")
    size_dictionary = basic.calculate_size_metrics(test_data)
    assert size_dictionary["Mean"] == 350.50

def test_size_median():
    test_dictionary = {}
    test_dictionary["File Size in Bytes"] = [455, 327, 315, 80, 540]
    test_data = pd.DataFrame.from_dict(test_dictionary, orient="columns")
    size_dictionary = basic.calculate_size_metrics(test_data)
    assert size_dictionary["Median"] == 327


def test_calculate_lines_added_metrics():
    test_dictionary = {}
    test_dictionary["Lines Added"] = [4, 12, 3, 30]
    test_data = pd.DataFrame.from_dict(test_dictionary, orient="columns")
    added_dictionary = basic.calculate_lines_added_metrics(test_data)
    assert len(added_dictionary) == 4


def test_lines_added_minimum():
    test_dictionary = {}
    test_dictionary["Lines Added"] = [4, 12, 3, 30]
    test_data = pd.DataFrame.from_dict(test_dictionary, orient="columns")
    added_dictionary = basic.calculate_lines_added_metrics(test_data)
    assert added_dictionary["Minimum"] == 3


def test_lines_added_maximum():
    test_dictionary = {}
    test_dictionary["Lines Added"] = [4, 12, 3, 30]
    test_data = pd.DataFrame.from_dict(test_dictionary, orient="columns")
    added_dictionary = basic.calculate_lines_added_metrics(test_data)
    assert added_dictionary["Maximum"] == 30


def test_lines_added_mean():
    test_dictionary = {}
    test_dictionary["Lines Added"] = [4, 12, 3, 30]
    test_data = pd.DataFrame.from_dict(test_dictionary, orient="columns")
    added_dictionary = basic.calculate_lines_added_metrics(test_data)
    assert added_dictionary["Mean"] == 12.25

def test_lines_added_median():
    test_dictionary = {}
    test_dictionary["Lines Added"] = [4, 12, 3, 30, 27]
    test_data = pd.DataFrame.from_dict(test_dictionary, orient="columns")
    added_dictionary = basic.calculate_lines_added_metrics(test_data)
    assert added_dictionary["Median"] == 12

def test_calculate_lines_removed_metrics():
    test_dictionary = {}
    test_dictionary["Lines Removed"] = [4, 12, 3, 30]
    test_data = pd.DataFrame.from_dict(test_dictionary, orient="columns")
    removed_dictionary = basic.calculate_lines_removed_metrics(test_data)
    assert len(removed_dictionary) == 4


def test_lines_removed_minimum():
    test_dictionary = {}
    test_dictionary["Lines Removed"] = [4, 12, 3, 30]
    test_data = pd.DataFrame.from_dict(test_dictionary, orient="columns")
    removed_dictionary = basic.calculate_lines_removed_metrics(test_data)
    assert removed_dictionary["Minimum"] == 3


def test_lines_removed_maximum():
    test_dictionary = {}
    test_dictionary["Lines Removed"] = [4, 12, 3, 30]
    test_data = pd.DataFrame.from_dict(test_dictionary, orient="columns")
    removed_dictionary = basic.calculate_lines_removed_metrics(test_data)
    assert removed_dictionary["Maximum"] == 30


def test_lines_removed_mean():
    test_dictionary = {}
    test_dictionary["Lines Removed"] = [4, 12, 3, 30]
    test_data = pd.DataFrame.from_dict(test_dictionary, orient="columns")
    removed_dictionary = basic.calculate_lines_removed_metrics(test_data)
    assert removed_dictionary["Mean"] == 12.25


def test_lines_removed_median():
    test_dictionary = {}
    test_dictionary["Lines Removed"] = [4, 12, 3, 30, 27]
    test_data = pd.DataFrame.from_dict(test_dictionary, orient="columns")
    removed_dictionary = basic.calculate_lines_removed_metrics(test_data)
    assert removed_dictionary["Median"] == 12
#TODO: tmpfs fixture to test download_https

# def test_download_https(tmp_path):
#     d = tmp_path / "repos"
#     repos_to_check = []
#     repository_list = ["https://github.com/gkapfham/meSMSage"]
#     directory = str(d)
#     print(directory)
#     path_list = download_repos.generate_save_path(repository_list, directory)
#     repository_amounts = download_repos.download_https(repository_list, path_list)
#     assert repository_amounts == 1

# def test_generate_file_list():
#     repository_path = "testActionTraction"
#     files_changed_list = traverse_repos.generate_file_list(repository_path)
#     assert len(files_changed_list) == 1

# def test_determine_actions_files():
#     repository_path = "testActionTraction"
#     files_changed_list = traverse_repos.generate_file_list(repository_path)
#     actions_files_list = traverse_repos.determine_actions_files(files_changed_list)
#     assert len(actions_files_list) == 1

# def test_iterate_actions_files():
#     repository_path = "testActionTraction"
#     files_changed_list = traverse_repos.generate_file_list(repository_path)
#     actions_files_list = traverse_repos.determine_actions_files(files_changed_list)
#     final_dataframe = traverse_repos.iterate_actions_files(actions_files_list)

# def test_iterate_actions_files():
#     repository_path = "testActionTraction"
#     files_changed_list = traverse_repos.generate_file_list(repository_path)
#     actions_files_list = traverse_repos.determine_actions_files(files_changed_list)
#     final_dataframe = traverse_repos.iterate_actions_files(actions_files_list)
#     number_columns = len(final_dataframe.columns)
#     number_columns = len(final_dataframe.columns)
#     assert number_columns == 8

