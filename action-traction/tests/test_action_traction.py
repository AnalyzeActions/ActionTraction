from action_traction import __version__
from action_traction import download_repos
from action_traction import traverse_repos


def test_version():
    assert __version__ == '0.1.0'

def test_generate_paths():
    repository_list = ["Repo_one", "Repo_two", "Repo_three"]
    directory = "home/mkapfhammer/Documents"
    path_list = download_repos.generate_save_path(repository_list, directory)
    assert len(path_list) == 3

#TODO: tmpfs fixture to test download_https

# def test_download_https():
#     repository_list = ["https://github.com/AnalyzeActions/testActionTraction"]
#     directory = "home/mkapfhammer/Documents/ActionTraction/action-traction/tests"
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

