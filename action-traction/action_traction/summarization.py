"""A python program to determine summary statistics relation to GitHub Actions configurations."""
from pydriller import Repository
from typing import List
import statistics
import pandas as pd
import datetime
from ordered_set import OrderedSet


def determine_repositories(initial_data):
    """Find each repository in the complete dataset of repository information."""
    # Create a list of all repositories
    repository_list = initial_data["repo"].tolist()
    # Find each unique repository name return the set
    repository_set = OrderedSet(repository_list)

    return repository_set


def determine_files_per_repo(initial_data, repository_set):
    """Determine all GitHub Actions files for a specific repository."""
    repo_file_dict = {}

    # Iterate through each unique repository name in the set
    for repository in repository_set:
        # Create a new dataset for each unique repository
        new_data = initial_data.loc[initial_data["repo"] == repository]
        # Make a list of each of the files for a unique repository
        file_list = new_data["file_changed"].tolist()
        # Determine each unique GitHub Actions file associated with a repository
        file_set = OrderedSet(file_list)
        # Create a dictionary with repository as key and corresponding files as value
        repo_file_dict[repository] = file_set

    return repo_file_dict


def determine_entire_repo_lifetime(repository_path: str):
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
            new_data = initial_data.loc[initial_data["file_changed"] == file]
            # Create a list of commit dates from intial dataset
            date_list = new_data["date"].tolist()

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
            lifetime_dictionary["repo"] = [repo]
            lifetime_dictionary["file_changed"] = [file]
            lifetime_dictionary["repo_lifetime"] = [repository_lifetime]
            lifetime_dictionary["file_lifetime"] = [file_lifetime]
            lifetime_dictionary["file_existence"] = percentage_of_lifetime

            for date in date_list:
                lifetime_dictionary["date"] = [date]

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
    dataframe_list = []
    size_dataframe = pd.DataFrame()

    # Iterate through the dictionary with repositories and corresponding files
    for repo, file_list in repo_file_dict.items():
        # Iterate through each file in a unqiue repository
        for file in file_list:
            # Create a new dataset for each file in a repo
            new_data = initial_data.loc[initial_data["file_changed"] == file]
            size_list = new_data["size_bytes"].tolist()

            # Generate summary statistics relating to file size
            minimum = min(size_list)
            maximum = max(size_list)
            mean = statistics.mean(size_list)
            median = statistics.median(size_list)
            st_dev = statistics.stdev(size_list)
            variance = statistics.variance(size_list)

            # Create dictionary for each repository with size summary stats
            size_dictionary["repo"] = [repo]
            size_dictionary["file_changed"] = [file]
            size_dictionary["min"] = [minimum]
            size_dictionary["max"] = [maximum]
            size_dictionary["mean"] = [mean]
            size_dictionary["median"] = [median]
            size_dictionary["standard_deviation"] = [st_dev]
            size_dictionary["variance"] = [variance]

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
    dataframe_list = []
    author_dataframe = pd.DataFrame()

    # Iterate through the dictionary with repositories and corresponding files
    for repo, file_list in repo_file_dict.items():
        # Iterate through each file in a unqiue repository
        for file in file_list:
            # Create a new dataset for each unique file
            new_data = initial_data.loc[initial_data["file_changed"] == file]
            # Create a list of authors for commits of each Action file
            author_list = new_data["author"].tolist()
            # Create a list of unique authors related to each Action file
            author_set = set(author_list)

            list_percentage_contributions = []

            # Iterate through each author in the set of unique authors
            for unique_author in author_set:
                # Count how many commits an author contributed to a repo's GitHub Actions
                unique_author_contribution = author_list.count(unique_author)
                # Determine percentage of author contribution
                author_percentage_contribution = (
                    (unique_author_contribution) / len(author_list) * 100
                )
                # Create list of author contribution percentage
                list_percentage_contributions.append(author_percentage_contribution)

                # Create dictionary with author summary stats
                author_dictionary["repo"] = [repo]
                author_dictionary["file_changed"] = [file]
                author_dictionary["author"] = [unique_author]
                author_dictionary[
                    "author_commits"
                ] = unique_author_contribution
                author_dictionary["author_contribution"] = [
                    author_percentage_contribution
                ]

                # Create pandas dataframe from dictionary
                initial_dataframe = pd.DataFrame.from_dict(
                    author_dictionary, orient="columns"
                )
                dataframe_list.append(initial_dataframe)

    # Create pandas dataframe with information for all repositories
    for result in dataframe_list:
        author_dataframe = author_dataframe.append(result)

    return author_dataframe


def calculate_committer_metrics(initial_data, repo_file_dict):
    """Determine summary statistics relating to committers of GitHub Actions files."""
    committer_dictionary = {}
    dataframe_list = []
    committer_dataframe = pd.DataFrame()

    # Iterate through the dictionary with repositories and corresponding files
    for repo, file_list in repo_file_dict.items():
        # Iterate through each file in a unqiue repository
        for file in file_list:
            # Create a new dataset for each unique file
            new_data = initial_data.loc[initial_data["file_changed"] == file]
            # Create a list of committers for each file
            committer_list = new_data["committer"].tolist()
            # Create a set of each unqiue committer associated with a Actions file
            committer_set = set(committer_list)

            list_percentage_contributions = []

            # Iterate through each of the committers in the set
            for unique_committer in committer_set:
                # Count how many commits a committer is associated with in a repository
                unique_committer_contribution = committer_list.count(unique_committer)
                # Determine percentage of contribution for a committer
                committer_percentage_contribution = (
                    (unique_committer_contribution) / len(committer_list) * 100
                )
                # Create a list of contribution percentages
                list_percentage_contributions.append(committer_percentage_contribution)

                # Create a dictionary for committer summary stats
                committer_dictionary["repo"] = [repo]
                committer_dictionary["file_changed"] = [file]
                committer_dictionary["committer"] = [unique_committer]
                committer_dictionary[
                    "committer_commits"
                ] = unique_committer_contribution
                committer_dictionary["committer_contribution"] = [
                    committer_percentage_contribution
                ]

                # Create a dataframe from committer summary stats dictionary for each repo
                initial_dataframe = pd.DataFrame.from_dict(
                    committer_dictionary, orient="columns"
                )
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
            new_data = initial_data.loc[initial_data["file_changed"] == file]
            # Create a list of lines added metrics for each file
            lines_added_list = new_data["lines_added"].tolist()

            # Generate summary statistics relating to lines added
            mean = statistics.mean(lines_added_list)
            median = statistics.median(lines_added_list)
            minimum = min(lines_added_list)
            maximum = max(lines_added_list)
            st_dev = statistics.stdev(lines_added_list)
            variance = statistics.variance(lines_added_list)

            # Create dictionary for each repository with lines added summary stats
            added_dictionary["repo"] = [repo]
            added_dictionary["file_changed"] = [file]
            added_dictionary["min"] = [minimum]
            added_dictionary["max"] = [maximum]
            added_dictionary["mean"] = [mean]
            added_dictionary["median"] = [median]
            added_dictionary["standard_deviation"] = [st_dev]
            added_dictionary["variance"] = [variance]

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
            new_data = initial_data.loc[initial_data["file_changed"] == file]
            # Create a list of lines removed metrics for each file
            lines_removed_list = new_data["lines_removed"].tolist()

            # Generate summary statistics relating to lines removed
            mean = statistics.mean(lines_removed_list)
            median = statistics.median(lines_removed_list)
            minimum = min(lines_removed_list)
            maximum = max(lines_removed_list)
            st_dev = statistics.stdev(lines_removed_list)
            variance = statistics.variance(lines_removed_list)

            # Create dictionary for each repository with lines removed summary stats
            removed_dictionary["repo"] = [repo]
            removed_dictionary["file_changed"] = [file]
            removed_dictionary["min"] = [minimum]
            removed_dictionary["max"] = [maximum]
            removed_dictionary["mean"] = [mean]
            removed_dictionary["median"] = [median]
            removed_dictionary["standard_deviation"] = [st_dev]
            removed_dictionary["variance"] = [variance]

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
            new_data = initial_data.loc[initial_data["file_changed"] == file]
            # Create list of commit messages relating to each file
            commit_message_list = new_data["commit_message"].tolist()

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
            commit_message_dictionary["repo"] = [repo]
            commit_message_dictionary["file_changed"] = [file]
            commit_message_dictionary["message_size"] = [size_message_list]
            commit_message_dictionary["min"] = [minimum]
            commit_message_dictionary["max"] = [maximum]
            commit_message_dictionary["mean"] = [mean]
            commit_message_dictionary["median"] = [median]
            commit_message_dictionary["standard_deviation"] = [st_dev]
            commit_message_dictionary["variance"] = [variance]

            # Create a dataframe from commit message dictionary
            initial_size_dataframe = pd.DataFrame.from_dict(commit_message_dictionary)
            dataframe_list.append(initial_size_dataframe)

    # Create a dataframe for commit messages with every repository and file
    for result in dataframe_list:
        commit_message_dataframe = commit_message_dataframe.append(result)

    return commit_message_dataframe


def determine_contributors(directory: str):
    """Determine who has contributed to GitHub Actions files."""
    csv_path = directory + "/final_data.csv"
    entire_data_path = directory + "/all_commit_data.csv"
    initial_data = pd.read_csv(csv_path)
    entire_repo_data = pd.read_csv(entire_data_path)
    repository_set = determine_repositories(initial_data)
    repo_file_dict = determine_files_per_repo(initial_data, repository_set)

    author_results = calculate_author_metrics(initial_data, repo_file_dict)
    committer_results = calculate_committer_metrics(initial_data, repo_file_dict)
    author_results.to_csv(directory + "/authors.csv")
    committer_results.to_csv(directory + "/committers.csv")

    contributors_results = contributors_enitre_repo(entire_repo_data, repository_set)

    complete_dataframe = author_results
    committers = committer_results["committer"].tolist()
    committer_number = committer_results["committer_commits"].tolist()
    committer_contribution = committer_results["committer_contribution"].tolist()
    all_contributors = contributors_results["contributor"].tolist()
    contributors_number = contributors_results["contributor_commits"].tolist()
    contributor_contribution = contributors_results["contributor_contribution"].tolist()

    complete_dataframe["committer"] = committers
    complete_dataframe["committer_commits"] = committer_number
    complete_dataframe["committer_contribution"] = committer_contribution
    
    # complete_dataframe["All Contributors"] = all_contributors
    # complete_dataframe["Contributor Commits"] = contributors_number
    # complete_dataframe["Contributions"] = contributor_contribution

    contribution_path = directory + "/contributors.csv"
    complete_dataframe.to_csv(contribution_path)

    return complete_dataframe


def contributors_enitre_repo(entire_repo_data, repo_set):
    """Determine the total contributors to a GitHub repository."""
    author_contributions_list = []
    percent_contributions = []
    contribution_data = pd.DataFrame()
    contributor_dictionary = {}
    repository_list = []
    all_authors = []
    dataframe_list = []

    for repo in repo_set:
        new_data = entire_repo_data.loc[entire_repo_data["repo"] == repo]

        # Determine all authors of commits in a repository
        author_list = new_data["author"].tolist()
        # Determine each unique author for a GitHub repository
        author_set = set(author_list)


        # Iterate through all unique authors and determine contribution
        for author in author_set:
            # Count how many commits an author is associated with in a repo
            author_contribution = author_list.count(author)
            # Calculate percentage of contribution based on commits
            author_percentage_contribution = ((author_contribution) / (len(author_list))) * 100

            author_contributions_list.append(author_contribution)
            percent_contributions.append(author_percentage_contribution)

            repository_list.append(repo)
            all_authors.append(author)

        # Create a dictionary for committer summary stats
        contributor_dictionary["repo"] = repository_list
        contributor_dictionary["contributor"] = all_authors
        contributor_dictionary["contributor_commits"] = author_contributions_list
        contributor_dictionary["committer_contribution"] = percent_contributions

        # Create a dataframe from committer summary stats dictionary for each repo
        initial_dataframe = pd.DataFrame.from_dict(
            contributor_dictionary, orient="columns"
        )
        dataframe_list.append(initial_dataframe)

    for data in dataframe_list:
        contribution_data = contribution_data.append(data)

    return contribution_data


def determine_all_files(entire_csv: str):
    """Determine what files were changed in each commit."""
    files_changed_dict = {}
    dataframe_list = []
    final_dataframe = pd.DataFrame()
    all_commits_repo = pd.read_csv(entire_csv)

    hash_list = all_commits_repo["hash"].tolist()
    hash_set = set(hash_list)
    repository_list = all_commits_repo["repo"].tolist()
    repository_set = set(repository_list)

    for repo in repository_set:
        first_dataset = all_commits_repo.loc[all_commits_repo["repo"] == repo]
        for unique_hash in hash_set:
            new_data = first_dataset.loc[first_dataset["hash"] == unique_hash]
            files_changed_per_commit = new_data["files_changed"].tolist()
            # files_changed_dict[unique_hash] = files_changed_per_commit

            files_changed_dict["repo"] = repo
            files_changed_dict["hash"] = unique_hash
            files_changed_dict["files_changed"] = [files_changed_per_commit]

            first_dataframe = pd.DataFrame.from_dict(files_changed_dict)

            dataframe_list.append(first_dataframe)
    
    for data in dataframe_list:
        final_dataframe = final_dataframe.append(data)
    
    return final_dataframe
