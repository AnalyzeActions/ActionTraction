from action_traction import __version__
from action_traction import download_repos


def test_version():
    assert __version__ == '0.1.0'

def test_generate_paths():
    repository_list = ["Repo_one", "Repo_two", "Repo_three"]
    directory = "home/mkapfhammer/Documents"
    path_list = download_repos.generate_save_path(repository_list, directory)
    assert len(path_list) == 3


# def test_download_https():
#     repository_list = ["Repo_one", "Repo_two", "Repo_three"]
#     directory = "home/mkapfhammer/Documents"
#     path_list = download_repos.generate_save_path(repository_list, directory)
#     repository_amounts = download_repos.download_https(repository_list, path_list)
#     assert repository_amounts == 3

# def test_generate_file_list():
#     repository_path = "home/mkapfhammer/Documents/predictiveWellness"
