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
    author_list = initial_data["Author"].tolist()


# def calculate_committer_metrics(initial_data):
    
# def calculate_branches_metrics(initial_data):

# def calculate_lines_added_metrics(initial_data):

# def calculate_lines_removed_metrics(initial_data):