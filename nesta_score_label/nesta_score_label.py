# -*- coding: utf-8 -*-

import re
import os.path
import pandas as pd
import joblib
import requests
from pathlib import Path

teams = [
    'Innovation Mapping',
    'RAP Innovation',
    'RAP International Innovation',
    'RAP Explorations',
    'Creative Economy (RAP and IP)',
    'Challenge Prizes',
    'Health Lab',
    'Skills',
    'RAP Explorations',
    'Innovation Programmes - Education',
    'Government Innovation (RAP and IP)'
]


team_threshold = 0.1

def load_model(name):
    """
        Loads the model from the model folder
        Returns: Classifier
    """
    data_folder =  Path(__file__).resolve().parent
    file_to_open = data_folder / 'models' / name
    return joblib.load(str(file_to_open))

def load_keywords():
    """
        Loads the keywords from the models folder
        Returns: list of strings
    """
    data_folder =  Path(__file__).resolve().parent
    file_to_open = data_folder / 'models' / 'saved_keywords.csv'
    with open(str(file_to_open), 'r') as file:
        all_unique_kws = [w for w in file.read().split('\n')[1:] if len(w)]
    return all_unique_kws

def len_tokenized_text(input_text):
    """
        Calculates number of words in text
        Returns: number
    """
    return len(input_text.split(" "))

def get_counting_cols(df, search_col_name, keyword_list):
    """
        Counts the occurances of keywords in a column of a dataframe
        Inputs are the dataframe, the column to count keywords,
        and the keyword list
        Returns: Dataframe
    """
    output_df = pd.DataFrame()
    for keyword in keyword_list:
        col_name = "{}_count_{}".format(search_col_name, keyword)
        output_df[col_name] = df[search_col_name].map(lambda x: x.count(keyword))
    return output_df

def tidy_text(input_string):
    """
        Cleans an input string
        Returns: string
    """
    if type(input_string) != str: return ""

    return (re.sub(r"[^\w\s]","",input_string)
              .replace("\n", " ")
              .replace("\r", "")
              .lower()
              .strip()
           )

def create_feature_matrix(data, all_unique_kws = None):
    """
        Given a list of proposals, and a list of keywords,
        We generate the feature matrix for each proposal
        Returns: Dataframe
    """

    # Convert to a pandas dataframe
    df = pd.DataFrame(data)

    # Load in the keywords
    if all_unique_kws == None:
        # Load the folder
        all_unique_kws = load_keywords()

    # Calculate the feature matrix
    df["project_name_clean"] = df["title"].map(tidy_text)
    df["description_clean"] = df["content"].map(tidy_text)
    df["project_name_clean_len"] = df["project_name_clean"].map(len_tokenized_text)
    df["description_clean_len"] = df["description_clean"].map(len_tokenized_text)

    project_name_clean_counts_df = get_counting_cols(df, "project_name_clean", all_unique_kws)
    decription_clean_counts_df = get_counting_cols(df, "description_clean", all_unique_kws)

    project_name_clean_counts_df["total_project_name_clean_count"] = project_name_clean_counts_df.sum(axis = 1)
    decription_clean_counts_df["total_description_clean_count"] = decription_clean_counts_df.sum(axis = 1)

    X = pd.concat([project_name_clean_counts_df, decription_clean_counts_df], axis = 1)

    X["description_clean_count_%_keywords"] = X["total_description_clean_count"] / df["description_clean_len"]
    X["project_name_clean_count_%_keywords"] = X["total_project_name_clean_count"] / df["project_name_clean_len"]

    return X.fillna(0)

def calculate_scores(feature_matrix):
    """
        Given a feature matrix for a number of proposals,
        we load the classifier in and generate the
        probabilities of interest for nesta
        Returns: array
    """
    nesta_model = load_model("nesta_model.pkl")
    probabilities = nesta_model.predict_proba(feature_matrix)[:,1]
    return probabilities

def binary_cols_to_concat_text(row, col_list, output_text_list):
    """
        Generates the label of a proposal
        Returns: string
    """
    label = ''
    for col, output  in zip(col_list, output_text_list):
        test = abs(row[col])
        if test.any()>0:
            if label != '':
                padding = ', '
            else:
                padding = ''
            label = label + padding + output
    return label

def calculate_labels(feature_matrix):
    """
        Given a feature matrix for a number of proposals,
        we load the classifier in and generate the
        labels, show which teams would be interested
        Returns: list
    """
    team_output_df = pd.DataFrame()

    for team in teams:
        # Load model
        team_model = load_model(f"team_model_{team}.pkl")

        # Make model & predictions
        team_y_test_proba = team_model.predict_proba(feature_matrix)[:,1]

        # Organise predictions
        team_y_test_pred = [1 if x > team_threshold else 0 for x in team_y_test_proba]
        prediction_df_col_names = ['index', f'proba_{team}', f'pred_{team}']
        predictions_array = list(zip(feature_matrix.index, team_y_test_proba, team_y_test_pred))
        predictions_df = pd.DataFrame(predictions_array, columns=prediction_df_col_names).set_index('index')

        # Add team predictions to teams dataframe
        team_output_df = pd.concat([team_output_df,predictions_df],axis=1)

    # Calculate the labels
    pred_teams = ['pred_' + s for s in teams]
    team_output_df['team_label'] = team_output_df.apply(binary_cols_to_concat_text, axis = 1, col_list = pred_teams, output_text_list = teams)

    return team_output_df['team_label']
