from pydriller import RepositoryMining
import io

def mine_yaml_files(repository_url):
    contents_list = []
    dates_list = []
    committer_list = []
    for commit in RepositoryMining(repository_url, filepath=".github/workflows/main.yml").traverse_commits():
        for modified_file in commit.modifications:
            # Add file contents to one comprehensive file
            with io.open("complete_yaml_history.yml", "a", encoding="utf-8") as f:
                if modified_file.source_code is None:
                    f.write("")
                else:
                    f.write(str(modified_file.source_code))
            # Add each file history to a list
            if modified_file.source_code is None:
                contents_list.append("")
            else:
                contents_list.append(str(modified_file.source_code))
            
        # Add dates of each GitHub Action file change to a list
        dates_list.append(commit.committer_date)
        # Add committer of each new file iteration to list
        committer_list.append(commit.committer)
            

    return contents_list, dates_list, committer_list

def determine_actions_lifetime(contents_list, dates_list):
    first_action_date = dates_list[0]
    last_action_date = dates_list[len(dates_list)-1]

    first_action = contents_list[0]
    last_action = contents_list[len(contents_list)-1]

    return first_action_date, first_action, last_action_date, last_action

