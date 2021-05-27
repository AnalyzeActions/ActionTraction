from pydriller import RepositoryMining
from pydriller import Repository

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
    for commit in Repository(repository_path, only_modifications_with_file_types=['.yml']).traverse_commits():
        author_list.append(commit.author.name)
        committer_list.append(commit.committer.name)
        date_list.append(commit.committer_date)
        branches_list.append(commit.branches)
        commit_messages_list.append(commit.msg)
        files_changed_list.append(commit.modifications)

        for modification in commit.modifications:
            source_code_list.append(str(modification.source_code))
            lines_added_list.append(modification.added)
            lines_deleted_list.append(modification.deleted)
            lines_of_code_list.append(modification.nloc)

