# -*- coding: utf-8 -*-

import pandas as pd
from nesta_score_label.utils import load_model, load_teams, team_threshold, binary_cols_to_concat_text

def calculate_scores(
    feature_matrix,
    models_folder=None
):
    """
        Given a feature matrix for a number of proposals,
        we load the classifier in and generate the
        probabilities of interest for nesta
        Returns: array
    """
    nesta_model = None
    if models_folder:
        nesta_model = load_model("nesta_model.pkl", models_folder)
    else:
        nesta_model = load_model("nesta_model.pkl")
    probabilities = nesta_model.predict_proba(feature_matrix)[:,-1]
    return probabilities

def calculate_labels(
    feature_matrix,
    models_folder=None
):
    """
        Given a feature matrix for a number of proposals,
        we load the classifier in and generate the
        labels, show which teams would be interested
        Returns: list
    """
    team_output_df = pd.DataFrame()

    teams = None
    if models_folder:
        teams = load_teams(models_folder)
    else:
        teams = load_teams()

    for team in teams:
        # Load model
        team_model = None
        if models_folder:
            team_model = load_model("team_model_" + team + ".pkl", models_folder)
        else:
            team_model = load_model("team_model_" + team + ".pkl")

        # Make model & predictions
        team_y_test_proba = team_model.predict_proba(feature_matrix)[:,-1]

        # Organise predictions
        team_y_test_pred = [1 if x > team_threshold else 0 for x in team_y_test_proba]
        prediction_df_col_names = ['index', 'proba_' + team, 'pred_' + team]
        predictions_array = list(zip(feature_matrix.index, team_y_test_proba, team_y_test_pred))
        predictions_df = pd.DataFrame(predictions_array, columns=prediction_df_col_names).set_index('index')

        # Add team predictions to teams dataframe
        team_output_df = pd.concat([team_output_df,predictions_df],axis=1)

    # Calculate the labels
    pred_teams = ['pred_' + s for s in teams]
    team_output_df['team_label'] = team_output_df.apply(binary_cols_to_concat_text, axis = 1, col_list = pred_teams, output_text_list = teams)

    return team_output_df['team_label']
