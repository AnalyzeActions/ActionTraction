import statistics

def calculate_size_metrics(initial_data):
    # print(initial_data["File Size in Bytes"])
    total_size = 0
    minimum = 0
    maximum = 0
    size_dictionary = {}
    size_list = initial_data["File Size in Bytes"].tolist()
    minimum = min(size_list)
    maximum = max(size_list)
    for index in range(0, len(size_list)):
        total_size = total_size + size_list[index]

    mean = total_size / len(size_list)
    median = statistics.median(size_list)

    size_dictionary["Minimum"] = minimum
    size_dictionary["Maximum"] = maximum
    size_dictionary["Mean"] = mean
    size_dictionary["Median"] = median

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
    

def calculate_branches_metrics(initial_data):
    branches_dictionary = {}
    branches_list = initial_data["Branches"].tolist()
    # print(branches_list)

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