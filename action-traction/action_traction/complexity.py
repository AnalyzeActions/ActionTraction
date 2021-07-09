from pydriller import Repository
from nested_lookup import nested_lookup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yaml
import math
import pathlib
import os

def determine_file_contents(repository_path: str):
    """Determine the GitHub Actions files in a given repository."""
    actions_files = []
    source_code_dict = {}
    dataframe_list = []
    file_name_list = []
    repository_path_list = []
    source_code_dataframe = pd.DataFrame()

    # Traverse the all of the commits in a given repository
    for commit in Repository(repository_path).traverse_commits():
        # Look at all commits with modified fiels
        for modification in commit.modified_files:
            # Drill repository for all commits where the GitHub Actions files were modified
            if ".github" in str(modification.new_path):
                actions_files.append(modification.source_code)
                file_name_list.append(modification.new_path)
                repository_path_list.append(repository_path)

                # Create a dictionary relating to source code of GitHub Actions file
                source_code_dict["Commit Hash"] = commit.hash
                source_code_dict["Repository"] = [repository_path]
                source_code_dict["File"] = [modification.new_path]
                source_code_dict["Source Code"] = modification.source_code
                source_code_dict["Date of Commit"] = commit.committer_date

                # Create a dataframe from the existing source code dictionary
                code_dataframe = pd.DataFrame.from_dict(source_code_dict)
                dataframe_list.append(code_dataframe)
    
    # Create a dataframe for entire repo and every file with source code
    for result in dataframe_list:
        source_code_dataframe = source_code_dataframe.append(result)
    
    return source_code_dataframe


def generate_abstract_syntax_trees(source_code_dataframe):
    """Generate abstract syntax trees from the source code of GitHub Actions files."""
    yaml_list = []

    # Generate a list of GitHub Actions source code
    source_code_list = source_code_dataframe["Source Code"].tolist()
    # Iterate through list of source code and convert to abstract syntax tree
    for source_code in source_code_list:
        if source_code is not None:
            try:
                parsed_yaml = yaml.safe_load(source_code)
                yaml_list.append(parsed_yaml)
            except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
                # Possible structure errors cause inability to parse for syntax tree generation
                yaml_list.append("Cannot Parse")
        # If unparseable, the file does not have any contents
        else:
            yaml_list.append("No file contents")
    
    source_code_dataframe["Parse Status"] = yaml_list

    # Generate a dataframe with source code abstract syntax trees
    yaml_dataframe = source_code_dataframe

    return yaml_dataframe


def determine_halstead_metrics(source_code_dataframe, yaml_dataframe):
    """Calculate Halstead metrics for a single repository and each file."""
    distinct_operators = 0
    distinct_operands = 0
    halstead_dict = {}
    vocab_list = []
    length_list = []
    volume_list = []
    difficulty_list = []
    effort_list = []
    halstead_dataframe = pd.DataFrame()

    # Generate a list of source code abstract syntax trees
    abstract_trees_list = yaml_dataframe["Parse Status"].tolist()
    # Generate a list of GitHub Actions files
    file_list = yaml_dataframe["File"].tolist()
    # Generate a list of commit dates
    date_list = source_code_dataframe["Date of Commit"].tolist()
    # Generate a list of commit hashes
    hash_list = source_code_dataframe["Commit Hash"].tolist()

    # Iterate through list of source code trees and search for operators and operands
    for tree in abstract_trees_list:
        # Find existing GitHub Actions used in .yml file
        uses_operator_list = nested_lookup("uses", tree)
        print("Found " + str(len(uses_operator_list)) + " unique GitHub Actions used.")
        # Find user defined commands used in .yml file
        runs_operator_list = nested_lookup("run", tree)
        print("Found " + str(len(runs_operator_list)) + " unique developer-specified commands used.")

        # Calculate the total amount of operators 
        total_operators = len(uses_operator_list) + len(runs_operator_list)

        # Determine distinct operators
        if len(uses_operator_list) != 0:
            # print("+1 for each existing action used")
            distinct_operators = distinct_operators + 1
            print("Found distinct operator 'uses'")
        if len(runs_operator_list) != 0:
            # print("+1 for each defined command used")
            distinct_operators = distinct_operators + 1
            print("Found distinct operator 'runs'")

        #TODO: Are "with" and "env" defined properly?
        # Find developer-defined commands used in .yml file
        name_operand_list = nested_lookup("name", tree)
        print("Found " + str(len(name_operand_list)) + " unique 'name'.")
        with_operand_list = nested_lookup("with", tree)
        print("Found " + str(len(with_operand_list)) + " unique 'with'.")
        env_operand_list = nested_lookup("env", tree)
        print("Found " + str(len(name_operand_list)) + " unique 'env'")
        
        total_operands = len(name_operand_list) + len(with_operand_list) + len(env_operand_list)

        if len(name_operand_list) != 0:
            distinct_operands = distinct_operands + 1
            print("Found distinct operand 'name' ")
        if len(with_operand_list) != 0:
            distinct_operands = distinct_operands + 1
            print("Found distinct operand 'with'")
        if len(env_operand_list) != 0 :
            distinct_operands = distinct_operands + 1
            print("Found distinct operand 'env'")

        # Calculate Halstead metrics and add to corresponding lists
        if distinct_operators != 0 and distinct_operands != 0 and total_operators != 0 and total_operands != 0:
            vocab = distinct_operators + distinct_operands
            vocab_list.append(vocab)
            length = total_operators + total_operands
            length_list.append(length)
            volume = length * (math.log(vocab, 2))
            volume_list.append(volume)
            difficulty = (distinct_operators / 2) * (total_operands / distinct_operands)
            difficulty_list.append(difficulty)
            effort = difficulty * volume
            effort_list.append(effort)
        # If no operators or operands are present, represent Halstead metrics as not a number
        else:
            vocab_list.append(np.nan)
            length_list.append(np.nan)
            volume_list.append(np.nan)
            difficulty_list.append(np.nan)
            effort_list.append(np.nan)

        distinct_operators = 0
        distinct_operands = 0

    # Create a dictionary with Halstead metrics for a repository and each .yml file
    halstead_dict["Hash"] = hash_list
    halstead_dict["Date"] = date_list
    halstead_dict["File"] = file_list
    halstead_dict["Vocabulary"] = vocab_list
    halstead_dict["Length"] = length_list
    halstead_dict["Volume"] = volume_list
    halstead_dict["Difficulty"] = difficulty_list
    halstead_dict["Effort"] = effort_list

    # Create a pandas dataframe from Halstead metrics dictionary
    halstead_data = pd.DataFrame.from_dict(halstead_dict)
    halstead_data.set_index('Date', inplace=True)
        
    # plot = halstead_data.plot()
    # figure = plot.get_figure()

    # figure.savefig("images/Halstead.png")

    return halstead_data


def determine_cyclomatic_complexity(yaml_dataframe, source_code_dataframe):
    """Determine the cyclomatic complexity of a repository."""
    total_complexity_list = []
    hash_list = []
    complexity_dict = {}

    # Create a list of source code abstract syntax trees
    abstract_trees_list = yaml_dataframe["Parse Status"].tolist()
    # Create a list of files for a repo
    file_list = yaml_dataframe["File"].tolist()
    # Create a list of date of commits
    date_list = source_code_dataframe["Date of Commit"].tolist()
    # Generate a list of commit hashes
    hash_list = source_code_dataframe["Commit Hash"].tolist()

    # Iterate through abstract syntax trees and count complexity metrics
    for tree in abstract_trees_list:
        if_amount = nested_lookup("if", tree)
        elif_amount = nested_lookup("elif", tree)
        matrix_amount = nested_lookup("matrix", tree)
        with_amount = nested_lookup("with", tree)
        env_amount = nested_lookup("env", tree)

        # TODO: Are with and envs correct here?
        if_complexity = len(if_amount)
        print("Found " + str(if_complexity) + " if statements, increasing complexity by " + str(if_complexity))
        elif_complexity = len(elif_amount)
        print("Found " + str(elif_complexity) + " elif statements, increasing complexity by " + str(elif_complexity))
        matrix_complexity = len(matrix_amount)
        print("Found " + str(matrix_complexity) + " matrices, increasing complexity by " + str(matrix_complexity))
        with_complexity = len(with_amount)
        print("Found " + str(with_complexity) + " with statements, increasing complexity by " + str(with_complexity))
        env_complexity = len(env_amount)
        print("Found " + str(env_complexity) + " environments, increasing complexity by " + str(env_complexity))

        # Calculate total cyclomatic complexity for a GitHub Actions file
        total_complexity = if_complexity + elif_complexity + matrix_complexity + with_complexity + env_complexity
        total_complexity_list.append(total_complexity)

    # Create a dictionary with cyclomatic complexity
    complexity_dict["Hash"] = hash_list
    complexity_dict["Date"] = date_list
    complexity_dict["File"] = file_list
    complexity_dict["Cyclomatic Complexity Score"] = total_complexity_list

    complexity_data = pd.DataFrame.from_dict(complexity_dict)
    complexity_data.set_index("Date", inplace=True)

    # plot = complexity_data.plot()
    # figure = plot.get_figure()

    # figure.savefig("images/CyclomaticComplexity.png")
    return complexity_data


def determine_raw_metrics(source_code_dataframe):
    """Determine SLOC metrics for a single repository."""
    comments_list = []
    lines_code = []
    lines_source_code = []
    total_lines_ratio_list = []
    ncss_ratio_list = []
    raw_metrics_dict = {}
    
    # Generate a list of GitHub Actions source code
    source_code_list = source_code_dataframe["Source Code"].tolist()
    # Generate a list of files in a repository
    file_list = source_code_dataframe["File"].tolist()
    # Generate a list of dates of commits 
    date_list = source_code_dataframe["Date of Commit"].tolist()
     # Generate a list of commit hashes
    hash_list = source_code_dataframe["Commit Hash"].tolist()

    # Iterate through the list of file source code
    for source_code in source_code_list:
        # Count the number of comments in a GitHub Actions file
        number_comments = source_code.count("#")
        comments_list.append(number_comments)

        # Count the number of source lines of code in a GitHub Actions file
        sloc = len(source_code.splitlines())
        lines_code.append(sloc)

        # Calculate number of non-commented lines of source code
        ncss = sloc - number_comments
        lines_source_code.append(ncss)

        # Determine ratios of comments to lines of code
        total_lines_ratio = (number_comments / sloc) * 100
        total_lines_ratio_list.append(total_lines_ratio)

        # Determine ratios of comments to non-commented lines of source code
        ncss_ratio = (number_comments / ncss) * 100
        ncss_ratio_list.append(ncss_ratio)

    # Create a dictionary with all raw metrics associated with a repository
    raw_metrics_dict["Hash"] = hash_list
    raw_metrics_dict["Date"] = date_list
    raw_metrics_dict["File"] = file_list
    raw_metrics_dict["Number of Comments"] = comments_list
    raw_metrics_dict["LOC"] = lines_code
    raw_metrics_dict["NCSS"] = lines_source_code
    raw_metrics_dict["Comments to Total Lines Comparison"] = total_lines_ratio_list
    raw_metrics_dict["Comments to Lines of Code Comparison"] = ncss_ratio_list

    # Create a datarame with the raw metrics dictionary
    raw_metrics_data = pd.DataFrame.from_dict(raw_metrics_dict)
    raw_metrics_data.set_index("Date", inplace=True)
    
    # plot = raw_metrics_data.plot()
    # figure = plot.get_figure()

    # figure.savefig("images/RawMetrics.png")
    return raw_metrics_data


def combine_metrics(halstead_data, complexity_data, raw_metrics_data):
    """Combine dataframes associated to Halstead metrics, Cyclomatic Complexity, and raw metrics."""
    
    # Create lists for all necessary metrics
    cyclomatic_complexity = complexity_data["Cyclomatic Complexity Score"].tolist()
    volume = halstead_data["Volume"].tolist()
    vocab = halstead_data["Vocabulary"].tolist()
    length = halstead_data["Length"].tolist()
    difficulty = halstead_data["Difficulty"].tolist()
    effort = halstead_data["Effort"].tolist()

    # Create a new pandas dataframe for combined data, started with raw metrics information
    combination = pd.DataFrame()
    combination = raw_metrics_data

    # Add cyclomatic complexity, and Halstead metrics to the combined dataframe
    combination["Cyclomatic Complexity"] = cyclomatic_complexity
    combination["Volume"] = volume
    combination["Vocabulary"] = vocab
    combination["Difficulty"] = difficulty
    combination["Effort"] = effort
    
    return combination


def calculate_maintainability(complete_dataframe, source_code_dataframe):
    """Calculate the maintainability index of a repository."""
    original_maintainability_list = []
    sei_maintainability_list = []
    vs_maintainability_list = []
    maintainability_dict = {}

    # Create a list of files in a repository
    file_list = complete_dataframe["File"].tolist()
    # Create a list of commit dates for a repository
    date_list = source_code_dataframe["Date of Commit"].tolist()
    # Generate a list of commit hashes
    hash_list = source_code_dataframe["Commit Hash"].tolist()
    
    # Set the index of the complete dataframe
    index = complete_dataframe.index

    # Iterate through the complete dataframe to gather Volume, Cyclomatic Complexity, NCSS and Number of Comments
    for index, row in complete_dataframe.iterrows():
        v = row["Volume"]
        cc = row["Cyclomatic Complexity"]
        ncss = row["NCSS"]
        c = row["Number of Comments"]
        
        # Calculate three different maintainability indexes
        if v != "NaN":
            # Calculate original_maintainability index
            original_maintainability = 171 - (5.2 * (np.log(v))) - (0.23 * cc) - (16.2 * (np.log(ncss)))
            original_maintainability_list.append(original_maintainability)
            # Calculate SEI maintainability index
            sei_maintainability = 171 - (5.2 * (np.log2(v))) - (0.23 * cc) - (16.2 * (np.log2(ncss))) + (50 * math.sin(math.sqrt(2.4 * c)))
            sei_maintainability_list.append(sei_maintainability)
            # Calculate Microsoft maintainability index
            vs_division = (171 - (5.2 * (np.log(v))) - (0.23 * cc) - (16.2 * (np.log(ncss))))/171
            vs_maintainability = max(0, 100 * vs_division)
            vs_maintainability_list.append(vs_maintainability)
        # if volume is recorded as not a number (NaN) represent maintainability as NaN
        else:
            original_maintainability_list.append("NaN")
            sei_maintainability_list.append("NaN")
            vs_maintainability_list.append("NaN")
    
    # Create a dictionary with maintainability indexes
    maintainability_dict["Hash"] = hash_list
    maintainability_dict["Date"] = date_list
    maintainability_dict["File"] = file_list
    maintainability_dict["Original Maintainability Index"] = original_maintainability_list
    maintainability_dict["SEI Maintainability Index"] = sei_maintainability_list
    maintainability_dict["Microsoft Maintainability Index"] = vs_maintainability_list

    # Create a pandas dataframe from a maintainability dictionary
    maintainability_data = pd.DataFrame.from_dict(maintainability_dict)
    
    # Set the index of the pandas dataframe to be the date of commit
    maintainability_data.set_index("Date", inplace=True)

    # plot = maintainability_data.plot()
    # figure = plot.get_figure()

    # figure.savefig("images/Maintainability.png")

    return maintainability_data


def combine_with_maintainability(complete_dataframe, maintainability_data):
    """Create a final complete dataframe with all complexity measures."""

    # Put maintainability indexes in a list
    original = maintainability_data["Original Maintainability Index"].tolist()
    sei = maintainability_data["SEI Maintainability Index"].tolist()
    microsoft = maintainability_data["Microsoft Maintainability Index"].tolist()

    # Add maintianability indexes to the dataframe with Halstead, SLOC and Cyclomatic Complexity metrics
    complete_dataframe["Origianl Maintainability Index"] = original
    complete_dataframe["SEI Maintainability Index"] = sei
    complete_dataframe["Microsoft Maintainability Index"] = microsoft

    # plot = complete_dataframe.plot()
    # figure = plot.get_figure()

    # figure.savefig("images/AllMetrics.png")

    return complete_dataframe


def iterate_through_directory(root_directory: str):
    """Generate a comprehensive dataframe of metrics for each repository in a specified directory."""
    repos_to_check = []
    dataframes_list = []
    complexity_dataframe = pd.DataFrame()
    final_dataframe = pd.DataFrame()

    # Generate a list of each subdirectory in the specified root directory
    for subdir, dirs, files in os.walk(root_directory):
        repos_to_check.append(dirs)
    
    # Iterate through each repository and perform methods to generate complexity scores
    for repository in repos_to_check[0]:
        path = pathlib.Path.home() / root_directory / repository
        source_code_dataframe = determine_file_contents(str(path))
        yaml_dataframe = generate_abstract_syntax_trees(source_code_dataframe)
        
        halstead_data = determine_halstead_metrics(yaml_dataframe, source_code_dataframe)
        complexity_data = determine_cyclomatic_complexity(yaml_dataframe, source_code_dataframe)
        raw_metrics_data = determine_raw_metrics(source_code_dataframe)
        combined_data = combine_metrics(halstead_data, complexity_data, raw_metrics_data)
        maintainability_data = calculate_maintainability(combined_data, source_code_dataframe)
        complexity_dataframe = combine_with_maintainability(combined_data, maintainability_data)
        # Add each repository-specific dataframe to a list
        dataframes_list.append(complexity_dataframe)
    
    # Create a comprehensive dataframe with individual repo dataframes
    for initial_data in dataframes_list:
        final_dataframe = final_dataframe.append(initial_data)
    
    return final_dataframe
