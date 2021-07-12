from pydriller import Repository
from typing import List
import statistics
import pandas as pd
import datetime


def determine_repositories(initial_data):
    """Find each repository in the complete dataset of repository information."""
    # Create a list of all repositories
    repository_list = initial_data["Repository"].tolist()
    # Find each unique repository name return the set
    repository_set = set(repository_list)
    
    return repository_set


def determine_files_per_repo(initial_data, repository_set):
    """Determine all GitHub Actions files for a specific repository."""
    repo_file_dict = {}
    
    # Iterate through each unique repository name in the set
    for repository in repository_set:
        # Create a new dataset for each unique repository
        new_data = initial_data.loc[initial_data['Repository'] == repository]
        # Make a list of each of the files for a unique repository
        file_list = new_data["File"].tolist()
        # Determine each unique GitHub Actions file associated with a repository
        file_set = set(file_list)
        # Create a dictionary with repository as key and corresponding files as value
        repo_file_dict[repository] = file_set

    return repo_file_dict


def determine_entire_repo_lifetime(repository_path:str):
    """Determine the time range of existence for a GitHub repository."""
    all_commit_dates = []
    # Iterate through commits in a repository and gather the dates of each commit
    for commit in Repository(repository_path).traverse_commits():
        all_commit_dates.append(commit.committer_date)
    
    # Beginning date corresponds to the first commit in the repository
    beginning_date = all_commit_dates[0]
    # Most recent date corresponds to the most recent commit in the repository
    most_recent_date = all_commit_dates[len(all_commit_dates) - 1]

    # Determine the lifetime of a repository by subtracting first commit and most recent commit
    repository_lifetime = most_recent_date - beginning_date

    return repository_lifetime



def calculate_file_lifetime(initial_data, repo_file_dict):
    """Determine the lifetime of each GitHub Actions file for a repository."""
    lifetime_dictionary = {}
    dataframe_list = []
    lifetime_dataframe = pd.DataFrame()

    # Iterate through the dictionary with repositories and corresponding files
    for repo, file_list in repo_file_dict.items():
        # Determine the lifetime of each repository using helper method
        repository_lifetime = determine_entire_repo_lifetime(repo)
        # Iterate through list of GitHub Actions files for a certain repository
        for file in file_list:
            # Create a new dataset for each unique file
            new_data = initial_data.loc[initial_data['File'] == file]
            # Create a list of commit dates from intial dataset 
            date_list = new_data["Date of Change"].tolist()
            
            # Determine the beginning of a file represented by the first commit where it existed
            file_start = date_list[0]
            # Determine the most recent commit related to a .yml file
            file_end = date_list[len(date_list) - 1]
            
            # Format datetime object
            file_start_datetime = datetime.datetime.fromisoformat(file_start)
            file_end_datetime = datetime.datetime.fromisoformat(file_end)

            # Determine the lifetime of the GitHub Action file 
            file_lifetime = file_end_datetime - file_start_datetime
            # Determine how long a Action file has existed in relation to the entire repo
            percentage_of_lifetime = (file_lifetime / repository_lifetime) * 100

            # Create a dictionary with all necessary information relating to lifetime
            lifetime_dictionary["Repository"] = [repo]
            lifetime_dictionary["File"] = [file]
            lifetime_dictionary["Repository Lifetime"] = [repository_lifetime]
            lifetime_dictionary["File Lifetime"] = [file_lifetime]
            lifetime_dictionary["Percentage of File Existence"] = percentage_of_lifetime

            for date in date_list:
                lifetime_dictionary["Date"] = [date]
            
            # Create a unique pandas dataframe for each repository dictionary
            initial_lifetime_dataframe = pd.DataFrame.from_dict(lifetime_dictionary)
            dataframe_list.append(initial_lifetime_dataframe)
        
    # Create a complete pandas dataframe with information relating to every repository
    for result in dataframe_list:
        lifetime_dataframe = lifetime_dataframe.append(result)

    return lifetime_dataframe


def calculate_size_metrics(initial_data, repo_file_dict):
    """Determine summary statistics relating to size of GitHub Actions files."""
    minimum = 0
    maximum = 0
    size_dictionary = {}
    final_dict = {}
    dataframe_list = []
    size_dataframe = pd.DataFrame()

    # Iterate through the dictionary with repositories and corresponding files
    for repo, file_list in repo_file_dict.items():
        # Iterate through each file in a unqiue repository
        for file in file_list:
            # Create a new dataset for each file in a repo
            new_data = initial_data.loc[initial_data['File'] == file]
            size_list = new_data["File Size in Bytes"].tolist()

            # Generate summary statistics relating to file size
            minimum = min(size_list)
            maximum = max(size_list)
            mean = statistics.mean(size_list)
            median = statistics.median(size_list)
            st_dev = statistics.stdev(size_list)
            variance = statistics.variance(size_list)
            
            # Create dictionary for each repository with size summary stats
            size_dictionary["Repository"] = [repo]
            size_dictionary["File"] = [file]
            size_dictionary["Minimum"] = [minimum]
            size_dictionary["Maximum"] = [maximum]
            size_dictionary["Mean"] = [mean]
            size_dictionary["Median"] = [median]
            size_dictionary["Standard Deviation"] = [st_dev]
            size_dictionary["Variance"] = [variance]

            # Create size stats dataframe for each repo
            initial_size_dataframe = pd.DataFrame.from_dict(size_dictionary)
            dataframe_list.append(initial_size_dataframe)
    
    # Create a complete pandas dataframe with information relating to every repository
    for result in dataframe_list:
        size_dataframe = size_dataframe.append(result)

    return size_dataframe


def calculate_author_metrics(initial_data, repo_file_dict):
    """Determine summary statistics relating to authors of GitHub Actions files."""
    author_dictionary = {}
    count_unique_authors = 0
    dataframe_list = []
    author_dataframe = pd.DataFrame()

    # Iterate through the dictionary with repositories and corresponding files
    for repo, file_list in repo_file_dict.items():
        # Iterate through each file in a unqiue repository
        for file in file_list:
            # Create a new dataset for each unique file
            new_data = initial_data.loc[initial_data['File'] == file]
            # Create a list of authors for commits of each Action file
            author_list = new_data["Author"].tolist()
            # Create a list of unique authors related to each Action file
            author_set = set(author_list)

            list_percentage_contributions = []

            # Iterate through each author in the set of unique authors
            for unique_author in author_set:
                # Count how many commits an author contributed to a repo's GitHub Actions
                unique_author_contribution = author_list.count(unique_author)
                # Determine percentage of author contribution
                author_percentage_contribution = (unique_author_contribution) / len(author_list) * 100
                # Create list of author contribution percentage
                list_percentage_contributions.append(author_percentage_contribution)
                
                # Create dictionary with author summary stats
                author_dictionary["Repository"] = [repo]
                author_dictionary["File"] = [file]
                author_dictionary["Author"] = [unique_author]
                author_dictionary["Number Corresponding Commits"] = unique_author_contribution
                author_dictionary["Percentage Contribution"] = [author_percentage_contribution]

                # Create pandas dataframe from dictionary
                initial_dataframe = pd.DataFrame.from_dict(author_dictionary, orient="columns")
                dataframe_list.append(initial_dataframe)
    
    # Create pandas dataframe with information for all repositories
    for result in dataframe_list:
        author_dataframe = author_dataframe.append(result)

    return author_dataframe


def calculate_committer_metrics(initial_data, repo_file_dict):
    """Determine summary statistics relating to committers of GitHub Actions files."""
    committer_dictionary = {}
    count_unique_committer = 0
    dataframe_list = []
    committer_dataframe = pd.DataFrame()

    # Iterate through the dictionary with repositories and corresponding files
    for repo, file_list in repo_file_dict.items():
        # Iterate through each file in a unqiue repository
        for file in file_list:
            # Create a new dataset for each unique file
            new_data = initial_data.loc[initial_data['File'] == file]
            # Create a list of committers for each file
            committer_list = new_data["Committer"].tolist()
            # Create a set of each unqiue committer associated with a Actions file
            committer_set = set(committer_list)

            list_percentage_contributions = []

            # Iterate through each of the committers in the set
            for unique_committer in committer_set:
                # Count how many commits a committer is associated with in a repository
                unique_committer_contribution = committer_list.count(unique_committer)
                # Determine percentage of contribution for a committer
                committer_percentage_contribution = (unique_committer_contribution) / len(committer_list) * 100
                # Create a list of contribution percentages
                list_percentage_contributions.append(committer_percentage_contribution)
                
                # Create a dictionary for committer summary stats
                committer_dictionary["Repository"] = [repo]
                committer_dictionary["File"] = [file]
                committer_dictionary["Committer"] = [unique_committer]
                committer_dictionary["Number Corresponding Commits"] = unique_committer_contribution
                committer_dictionary["Percentage Contribution"] = [committer_percentage_contribution]

                # Create a dataframe from committer summary stats dictionary for each repo
                initial_dataframe = pd.DataFrame.from_dict(committer_dictionary, orient="columns")
                dataframe_list.append(initial_dataframe)
    
    # Create a dataframe for each repo and committer summary stats
    for result in dataframe_list:
        committer_dataframe = committer_dataframe.append(result)

    return committer_dataframe


def calculate_lines_added_metrics(initial_data, repo_file_dict):
    """Determine summary statistics relating to lines added in a GitHub Actions file."""
    added_dictionary = {}
    dataframe_list = []
    added_dataframe = pd.DataFrame()

    # Iterate through the dictionary with repositories and corresponding files
    for repo, file_list in repo_file_dict.items():
        # Iterate through each file in a unqiue repository
        for file in file_list:
            # Create a new dataset for each unique file
            new_data = initial_data.loc[initial_data['File'] == file]
            # Create a list of lines added metrics for each file
            lines_added_list = new_data["Lines Added"].tolist()

            # Generate summary statistics relating to lines added
            mean = statistics.mean(lines_added_list)
            median = statistics.median(lines_added_list)
            minimum = min(lines_added_list)
            maximum = max(lines_added_list)
            st_dev = statistics.stdev(lines_added_list)
            variance = statistics.variance(lines_added_list)

            # Create dictionary for each repository with lines added summary stats
            added_dictionary["Repository"] = [repo]
            added_dictionary["File"] = [file]
            added_dictionary["Minimum"] = [minimum]
            added_dictionary["Maximum"] = [maximum]
            added_dictionary["Mean"] = [mean]
            added_dictionary["Median"] = [median]
            added_dictionary["Standard Deviation"] = [st_dev]
            added_dictionary["Variance"] = [variance]

            # Create a dataframe from lines added summary stats dictionary
            initial_size_dataframe = pd.DataFrame.from_dict(added_dictionary)
            dataframe_list.append(initial_size_dataframe)

    # Create a dataframe with lines added summary stats for each repository and file
    for result in dataframe_list:
        added_dataframe = added_dataframe.append(result)

    return added_dataframe


def calculate_lines_removed_metrics(initial_data, repo_file_dict):
    """Determine summary statistics related to lines removed in a GitHub Actions file."""
    removed_dictionary = {}
    dataframe_list = []
    removed_dataframe = pd.DataFrame()

    # Iterate through the dictionary with repositories and corresponding files
    for repo, file_list in repo_file_dict.items():
        # Iterate through each file in a unqiue repository
        for file in file_list:
            # Create a new dataset for each unique file
            new_data = initial_data.loc[initial_data['File'] == file]
            # Create a list of lines removed metrics for each file
            lines_removed_list = new_data["Lines Removed"].tolist()

            # Generate summary statistics relating to lines removed
            mean = statistics.mean(lines_removed_list)
            median = statistics.median(lines_removed_list)
            minimum = min(lines_removed_list)
            maximum = max(lines_removed_list)
            st_dev = statistics.stdev(lines_removed_list)
            variance = statistics.variance(lines_removed_list)

            # Create dictionary for each repository with lines removed summary stats
            removed_dictionary["Repository"] = [repo]
            removed_dictionary["File"] = [file]
            removed_dictionary["Minimum"] = [minimum]
            removed_dictionary["Maximum"] = [maximum]
            removed_dictionary["Mean"] = [mean]
            removed_dictionary["Median"] = [median]
            removed_dictionary["Standard Deviation"] = [st_dev]
            removed_dictionary["Variance"] = [variance]

            # Create a dataframe from lines removed summary stats dictionary
            initial_size_dataframe = pd.DataFrame.from_dict(removed_dictionary)
            dataframe_list.append(initial_size_dataframe)

    # Create a dataframe with lines removed summary stats for each repository and file
    for result in dataframe_list:
        removed_dataframe = removed_dataframe.append(result)

    return removed_dataframe


def calculate_commit_message_metrics(initial_data, repo_file_dict):
    """Determine summary statistics related to commit messages relating to GitHub Actions files."""
    commit_message_dictionary = {}
    dataframe_list = []
    commit_message_dataframe = pd.DataFrame()

    # Iterate through the dictionary with repositories and corresponding files
    for repo, file_list in repo_file_dict.items():
        # Iterate through each file in a unqiue repository
        for file in file_list:
            # Create a new dataset for each unique file
            new_data = initial_data.loc[initial_data['File'] == file]
            # Create list of commit messages relating to each file
            commit_message_list = new_data["Commit Message"].tolist()

            size_message_list = []

            # Iterate through each of the commit messages in the list
            for message in commit_message_list:
                # Determine the size of each commit message and add to list
                size_message_list.append(len(message))

            # Generate summary statistics relating to size of commit message
            mean = statistics.mean(size_message_list)
            median = statistics.median(size_message_list)
            minimum = min(size_message_list)
            maximum = max(size_message_list)
            st_dev = statistics.stdev(size_message_list)
            variance = statistics.variance(size_message_list)

            # Create dictionary of summary statistics relating to size of commit message
            commit_message_dictionary["Repository"] = [repo]
            commit_message_dictionary["File"] = [file]
            commit_message_dictionary["Commit Message Size"] = [size_message_list]
            commit_message_dictionary["Minimum"] = [minimum]
            commit_message_dictionary["Maximum"] = [maximum]
            commit_message_dictionary["Mean"] = [mean]
            commit_message_dictionary["Median"] = [median]
            commit_message_dictionary["Standard Deviation"] = [st_dev]
            commit_message_dictionary["Variance"] = [variance]

            # Create a dataframe from commit message dictionary
            initial_size_dataframe = pd.DataFrame.from_dict(commit_message_dictionary)
            dataframe_list.append(initial_size_dataframe)

    # Create a dataframe for commit messages with every repository and file
    for result in dataframe_list:
        commit_message_dataframe = commit_message_dataframe.append(result)

    return commit_message_dataframe
            
def perform_specified_summarization(specified_metrics: List[str], directory: str):
    csv_path = directory + "/minedRepos.csv"
    initial_data = pd.read_csv(csv_path)
    repository_set = determine_repositories(initial_data)
    repo_file_dict = determine_files_per_repo(initial_data, repository_set)

    if "Modifiers" in specified_metrics:
        author_results = calculate_author_metrics(initial_data, repo_file_dict)
        committer_results = calculate_committer_metrics(initial_data, repo_file_dict)
        print(author_results)
        print(committer_results)
    if "Size" in specified_metrics:
        size_results = calculate_size_metrics(initial_data, repo_file_dict)
        print(size_results)
    if "Lifetime" in specified_metrics:
        lifetime_results = calculate_file_lifetime(initial_data, repo_file_dict)
        print(lifetime_results)
    if "Diff" in specified_metrics:
        added_results = calculate_lines_added_metrics(initial_data, repo_file_dict)
        removed_results = calculate_lines_removed_metrics(initial_data, repo_file_dict)
        print(added_results)
        print(removed_results)
    if "Messages" in specified_metrics:
        messages_results = calculate_commit_message_metrics(initial_data, repo_file_dict)
        print(messages_results)
