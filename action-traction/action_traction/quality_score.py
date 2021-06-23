from pydriller import Repository
from nested_lookup import nested_lookup
import numpy as np
import os
import pathlib
import pandas as pd
import yaml
import re
import math

def determine_file_contents(repository_path: str):
    actions_files = []
    source_code_dict = {}
    dataframe_list = []
    file_name_list = []
    repository_path_list = []
    source_code_dataframe = pd.DataFrame()
    for commit in Repository(repository_path).traverse_commits():
        for modification in commit.modified_files:
            if ".github" in str(modification.new_path):
                actions_files.append(modification.source_code)
                file_name_list.append(modification.new_path)
                repository_path_list.append(repository_path)

                source_code_dict["Repository"] = [repository_path]
                source_code_dict["File"] = [modification.new_path]
                source_code_dict["Source Code"] = modification.source_code
                source_code_dict["Date of Commit"] = commit.committer_date
                code_dataframe = pd.DataFrame.from_dict(source_code_dict)
                dataframe_list.append(code_dataframe)
    for result in dataframe_list:
        source_code_dataframe = source_code_dataframe.append(result)
    return source_code_dataframe


def generate_abstract_syntax_trees(source_code_dataframe):
    yaml_list = []
    source_code_list = source_code_dataframe["Source Code"].tolist()
    for source_code in source_code_list:
        if source_code is not None:
            try:
                parsed_yaml = yaml.safe_load(source_code)
                yaml_list.append(parsed_yaml)
            except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
                yaml_list.append("Cannot Parse")
        else:
            yaml_list.append("No file contents")
    source_code_dataframe["Parse Status"] = yaml_list
    yaml_dataframe = source_code_dataframe
    
    # yaml_dataframe.to_csv(csv_url)
    return yaml_dataframe

def determine_halstead_metrics(yaml_dataframe):
    distinct_operators = 0
    distinct_operands = 0
    halstead_dict = {}
    vocab_list = []
    length_list = []
    volume_list = []
    difficulty_list = []
    effort_list = []
    abstract_trees_list = yaml_dataframe["Parse Status"].tolist()
    file_list = yaml_dataframe["File"].tolist()

    # print(abstract_trees_list[4])
    for tree in abstract_trees_list:
        # print("Start of Tree")
        # print(tree)
        uses_operator_list = nested_lookup("uses", tree)
        runs_operator_list = nested_lookup("run", tree)
        total_operators = len(uses_operator_list) + len(runs_operator_list)
        #TODO: Is this boolean working properly??
        if len(uses_operator_list) != 0:
            distinct_operators = distinct_operators + 1
        if len(runs_operator_list) != 0:
            distinct_operators = distinct_operators + 1

        name_operand_list = nested_lookup("name", tree)
        with_operand_list = nested_lookup("with", tree)
        env_operand_list = nested_lookup("env", tree)

        total_operands = len(name_operand_list) + len(with_operand_list) + len(env_operand_list)

        #TODO: Is this boolean working properly??
        if len(name_operand_list) != 0:
            distinct_operands = distinct_operands + 1
        if len(with_operand_list) != 0:
            distinct_operands = distinct_operands + 1
        if len(env_operand_list) != 0 :
            distinct_operands = distinct_operands + 1
        
        # print("Distinct Operators " + str(distinct_operators))
        # print("Distinct Operands " + str(distinct_operands))
        # print("Total Operators " + str(total_operators))
        # print("Total Operands " + str(total_operands))

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
            # print(volume)
        else:
            vocab_list.append("NaN")
            length_list.append("NaN")
            volume_list.append("NaN")
            difficulty_list.append("NaN")
            effort_list.append("NaN")

        distinct_operators = 0
        distinct_operands = 0

    halstead_dict["File"] = file_list
    halstead_dict["Vocabulary"] = vocab_list
    halstead_dict["Length"] = length_list
    halstead_dict["Volume"] = volume_list
    halstead_dict["Difficulty"] = difficulty_list
    halstead_dict["Effort"] = effort_list

    halstead_data = pd.DataFrame.from_dict(halstead_dict)
    return halstead_data


def determine_cyclomatic_complexity(yaml_dataframe):
    total_complexity_list = []
    complexity_dict = {}
    abstract_trees_list = yaml_dataframe["Parse Status"].tolist()
    file_list = yaml_dataframe["File"].tolist()

    for tree in abstract_trees_list:
        if_amount = nested_lookup("if", tree)
        elif_amount = nested_lookup("elif", tree)
        matrix_amount = nested_lookup("matrix", tree)
        with_amount = nested_lookup("with", tree)
        env_amount = nested_lookup("env", tree)
        #TODO: Boolean operators

        if_complexity = len(if_amount)
        elif_complexity = len(elif_amount)
        matrix_complexity = len(matrix_amount)
        with_complexity = len(with_amount)
        env_complexity = len(env_amount)

        total_complexity = if_complexity + elif_complexity + matrix_complexity + with_complexity + env_complexity
        total_complexity_list.append(total_complexity)

    complexity_dict["File"] = file_list
    complexity_dict["Cyclomatic Complexity Score"] = total_complexity_list

    complexity_data = pd.DataFrame.from_dict(complexity_dict)

    return complexity_data


def determine_raw_metrics(source_code_dataframe):
    comments_list = []
    lines_code = []
    lines_source_code = []
    total_lines_ratio_list = []
    ncss_ratio_list = []
    raw_metrics_dict = {}
    source_code_list = source_code_dataframe["Source Code"].tolist()
    file_list = source_code_dataframe["File"].tolist()

    # print(source_code_list[0])
    for source_code in source_code_list:
        number_comments = source_code.count("#")
        comments_list.append(number_comments)

        sloc = len(source_code.splitlines())
        lines_code.append(sloc)

        ncss = sloc - number_comments
        lines_source_code.append(ncss)

        total_lines_ratio = (number_comments / sloc) * 100
        total_lines_ratio_list.append(total_lines_ratio)

        ncss_ratio = (number_comments / ncss) * 100
        ncss_ratio_list.append(ncss_ratio)


    raw_metrics_dict["File"] = file_list
    raw_metrics_dict["Number of Comments"] = comments_list
    raw_metrics_dict["LOC"] = lines_code
    raw_metrics_dict["NCSS"] = lines_source_code
    raw_metrics_dict["Comments to Total Lines Comparison"] = total_lines_ratio_list
    raw_metrics_dict["Comments to Lines of Code Comparison"] = ncss_ratio_list

    raw_metrics_data = pd.DataFrame.from_dict(raw_metrics_dict)

    return raw_metrics_data


def combine_metrics(halstead_data, complexity_data, raw_metrics_data):
    cyclomatic_complexity = complexity_data["Cyclomatic Complexity Score"].tolist()
    volume = halstead_data["Volume"].tolist()
    vocab = halstead_data["Vocabulary"].tolist()
    length = halstead_data["Length"].tolist()
    difficulty = halstead_data["Difficulty"].tolist()
    effort = halstead_data["Effort"].tolist()

    combination = pd.DataFrame()
    combination = raw_metrics_data
    combination["Cyclomatic Complexity"] = cyclomatic_complexity
    combination["Volume"] = volume
    combination["Vocabulary"] = vocab
    combination["Difficulty"] = difficulty
    combination["Effort"] = effort
    
    return combination


def calculate_maintainability(complete_dataframe):
    original_maintainability_list = []
    sei_maintainability_list = []
    vs_maintainability_list = []
    maintainability_dict = {}
    file_list = complete_dataframe["File"].tolist()
    for index, row in complete_dataframe.iterrows():
        v = row["Volume"]
        cc = row["Cyclomatic Complexity"]
        ncss = row["NCSS"]
        c = row["Number of Comments"]

        if v != "NaN":
            original_maintainability = 171 - (5.2 * (np.log(v))) - (0.23 * cc) - (16.2 * (np.log(ncss)))
            original_maintainability_list.append(original_maintainability)
            sei_maintainability = 171 - (5.2 * (np.log2(v))) - (0.23 * cc) - (16.2 * (np.log2(ncss))) + (50 * math.sin(math.sqrt(2.4 * c)))
            sei_maintainability_list.append(sei_maintainability)
            vs_division = (171 - (5.2 * (np.log(v))) - (0.23 * cc) - (16.2 * (np.log(ncss))))/171
            vs_maintainability = max(0, 100 * vs_division)
            vs_maintainability_list.append(vs_maintainability)
        else:
            original_maintainability_list.append("NaN")
            sei_maintainability_list.append("NaN")
            vs_maintainability_list.append("NaN")
        
    maintainability_dict["File"] = file_list
    maintainability_dict["Original Maintainability Index"] = original_maintainability_list
    maintainability_dict["SEI Maintainability Index"] = sei_maintainability_list
    maintainability_dict["Microsoft Maintainability Index"] = vs_maintainability_list

    maintainability_data = pd.DataFrame.from_dict(maintainability_dict)
    return maintainability_data


def combine_with_maintainability(complete_dataframe, maintainability_data):
    final_dataframe = pd.DataFrame()
    original = maintainability_data["Original Maintainability Index"].tolist()
    sei = maintainability_data["SEI Maintainability Index"].tolist()
    microsoft = maintainability_data["Microsoft Maintainability Index"].tolist()

    final_dataframe = complete_dataframe

    complete_dataframe["Origianl Maintainability Index"] = original
    complete_dataframe["SEI Maintainability Index"] = sei
    complete_dataframe["Microsoft Maintainability Index"] = microsoft

    return complete_dataframe


def final_score(repository_path, score_choices):
    source_code_dataframe = determine_file_contents(repository_path)
    yaml_dataframe = generate_abstract_syntax_trees(source_code_dataframe)
    
    if "Halstead" in score_choices:
        halstead_data = determine_halstead_metrics(yaml_dataframe)
        print(halstead_data)
    if "Complexity" in score_choices:
        complexity_data = determine_cyclomatic_complexity(yaml_dataframe)
        print(complexity_data)
    if "RawMetrics" in score_choices:
        raw_metrics_data = determine_raw_metrics(source_code_dataframe)
        print(raw_metrics_data)
    if "Maintainability" in score_choices:
        halstead_data = determine_halstead_metrics(yaml_dataframe)
        complexity_data = determine_cyclomatic_complexity(yaml_dataframe)
        raw_metrics_data = determine_raw_metrics(source_code_dataframe)
        combined_data = combine_metrics(halstead_data, complexity_data, raw_metrics_data)
        maintainability_data = calculate_maintainability(combined_data)
        print(maintainability_data)
    if "AllMetrics" in score_choices:
        halstead_data = determine_halstead_metrics(yaml_dataframe)
        complexity_data = determine_cyclomatic_complexity(yaml_dataframe)
        raw_metrics_data = determine_raw_metrics(source_code_dataframe)
        combined_data = combine_metrics(halstead_data, complexity_data, raw_metrics_data)
        maintainability_data = calculate_maintainability(combined_data)
        final_dataframe = combine_with_maintainability(combined_data, maintainability_data)
        print(final_dataframe)
