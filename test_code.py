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

        for modification in commit.modifications:
            count = count + 1
            if modification.source_code is None:
                source_code_list.append("")
            else:
                source_code_list.append(str(modification.source_code))

            lines_added_list.append(modification.added)
            lines_deleted_list.append(modification.removed)
            lines_of_code_list.append(modification.nloc)

    print(len(author_list))
    print(count)


if __name__ == "__main__":
    iterate_commits("/home/mkapfhammer/Documents/predictiveWellness")