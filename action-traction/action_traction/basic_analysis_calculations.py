import statistics
import pandas as pd

def determine_repositories(initial_data):
    repository_list = initial_data["Repository"].tolist()
    repository_set = set(repository_list)
    return repository_set


def determine_files_per_repo(initial_data, repository_set):
    repo_file_dict = {}
    for repository in repository_set:
        new_data = initial_data.loc[initial_data['Repository'] == repository]
        # print(new_data)
        file_list = new_data["File"].tolist()
        file_set = set(file_list)
        repo_file_dict[repository] = file_set
    # print(repo_file_dict)
    return repo_file_dict


def calculate_size_metrics(initial_data, repo_file_dict):
    # print(initial_data["File Size in Bytes"])
    # total_size = 0
    minimum = 0
    maximum = 0
    size_dictionary = {}
    final_dict = {}
    dataframe_list = []
    size_dataframe = pd.DataFrame()
    for repo, file_list in repo_file_dict.items():
        for file in file_list:
            new_data = initial_data.loc[initial_data['File'] == file]
            size_list = new_data["File Size in Bytes"].tolist()
            print(size_list)
            minimum = min(size_list)
            maximum = max(size_list)
            total_size = 0
            for index in range(0, len(size_list)):
                total_size = total_size + size_list[index]
            print(total_size)
            mean = total_size / len(size_list)
            median = statistics.median(size_list)
            
            size_dictionary["Repository"] = [repo]
            size_dictionary["File"] = [file]
            size_dictionary["Minimum"] = [minimum]
            size_dictionary["Maximum"] = [maximum]
            size_dictionary["Mean"] = [mean]
            size_dictionary["Median"] = [median]
            initial_size_dataframe = pd.DataFrame.from_dict(size_dictionary)
            dataframe_list.append(initial_size_dataframe)
    for result in dataframe_list:
        size_dataframe = size_dataframe.append(result)
    print(size_dataframe)
    return size_dictionary


def calculate_author_metrics(initial_data):
    author_dictionary = {}
    author_list = initial_data["Author"].tolist()
    author_set = set(author_list)
    count_unique_authors = 0
    for unique_author in author_set:
        count_unique_authors = author_list.count(unique_author)
        author_dictionary[unique_author] = count_unique_authors
        author_percentage_contribution = (count_unique_authors / len(author_list)) * 100
        author_dictionary[unique_author + " Percentage Contribution"] = author_percentage_contribution
    return author_dictionary


def calculate_committer_metrics(initial_data):
    committer_dictionary = {}
    committer_list = initial_data["Author"].tolist()
    committer_set = set(committer_list)
    count_unique_authors = 0
    for unique_committer in committer_set:
        count_unique_committers = committer_list.count(unique_committer)
        committer_dictionary[unique_committer] = count_unique_committers
        committer_percentage_contribution = (count_unique_committers / len(committer_list)) * 100
        committer_dictionary[unique_committer + " Percentage Contribution"] = committer_percentage_contribution
    # print(committer_dictionary)
    

# def calculate_branches_metrics(initial_data):
#     branches_dictionary = {}
#     branches_list = initial_data["Branches"].tolist()
#     for branch in branches_list:
#         print(type(branch))

def calculate_lines_added_metrics(initial_data):
    added_dictionary = {}
    lines_added_list = initial_data["Lines Added"].tolist()
    minimum = min(lines_added_list)
    maximum = max(lines_added_list)
    total_lines_added = 0
    for index in range(0, len(lines_added_list)):
        total_lines_added = total_lines_added + lines_added_list[index]

    mean = total_lines_added / len(lines_added_list)
    median = statistics.median(lines_added_list)

    added_dictionary["Minimum"] = minimum
    added_dictionary["Maximum"] = maximum
    added_dictionary["Mean"] = mean
    added_dictionary["Median"] = median

    return added_dictionary

def calculate_lines_removed_metrics(initial_data):
    removed_dictionary = {}
    lines_removed_list = initial_data["Lines Removed"].tolist()
    minimum = min(lines_removed_list)
    maximum = max(lines_removed_list)
    total_lines_removed = 0
    for index in range(0, len(lines_removed_list)):
        total_lines_removed = total_lines_removed + lines_removed_list[index]
    
    mean = total_lines_removed / len(lines_removed_list)
    median = statistics.median(lines_removed_list)

    removed_dictionary["Minimum"] = minimum
    removed_dictionary["Maximum"] = maximum
    removed_dictionary["Mean"] = mean
    removed_dictionary["Median"] = median

    return removed_dictionary

def perform_specified_summarization(specified_metrics, initial_data):
    if "Modifiers" in specified_metrics:
        author_results = calculate_author_metrics(initial_data)
        committer_results = calculate_committer_metrics(initial_data)
        print(author_results)
        print(committer_results)
    if "Size" in specified_metrics:
        size_results = calculate_size_metrics(initial_data)
        print(size_results)
    # if "Lifetime" in specified_metrics:
    #     lifetime_results = calculate_lifetime_metrics(initial_data)
    # if "Diff" in specified_metrics:
    #     added_results = calculate_lines_added_metrics(initial_data)
    #     removed_results = calculate_lines_removed_metrics(initial_data)
    #     print(added_results)
    #     print(removed_results)