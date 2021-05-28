from typing import List 
from pathlib import Path
import pathlib
import os
import git

# from pydriller import Repository
from pydriller import RepositoryMining


def iterate_commits(repository_path):
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
    count = 0
    for commit in RepositoryMining(repository_path, only_modifications_with_file_types=['.yml']).traverse_commits():
        author_list.append(commit.author.name)
        committer_list.append(commit.committer.name)
        date_list.append(commit.committer_date)
        branches_list.append(commit.branches)
        commit_messages_list.append(commit.msg)
        files_changed_list.append(commit.modifications)

        # print(files_changed_list)
        for m in commit.modifications:
            count = count + 1
            if count == 1:
                print(
                    # m.__dict__
                    m._new_path
                )

    # print(len(author_list))
    # print(count)

def download_https(repository_list: List, save_path: Path):
    # Clone a remote repository using https
    for repo in repository_list:
        repo_name = os.path.splitext(os.path.basename(repo))[0]
        # print(repo_name)
        # path = pathlib.Path.home() / save_path / repo_name
        path = save_path / repo_name
        git.Repo.clone_from(repo, path)

if __name__ == "__main__":
    # iterate_commits("/home/mkapfhammer/Documents/predictiveWellness")
    repos = ["https://github.com/gkapfham/meSMSage"]
    download_https(repos, "~/Documents")