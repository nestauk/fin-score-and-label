# -*- coding: utf-8 -*-

import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble.forest import RandomForestClassifier
from nesta_score_label.utils import create_feature_matrix, team_threshold

try:
    from pathlib import Path
except:
    from pathlib2 import Path

models_folder = Path(__file__).resolve().parent / 'models'

def remove_old_models():
    """
        Removes all the pickled models from the models folder
    """
    for x in models_folder.iterdir():
        if x.is_file() and x.suffix == '.pkl':
            os.remove(str(x))

def relabel_input_data_columns(input_data, team_groups):
    """
        Renames the input data team columns names
        with new updated names
        Returns: Dataframe
    """
    for output_col_name in team_groups['new_name'].unique():
        input_col_names = list(team_groups[team_groups.new_name == output_col_name].old_name)
        input_data[output_col_name] = input_data[input_col_names].sum(axis=1).map(lambda x: 1 if x>0 else 0)

    dropped_cols = set(team_groups['old_name']).difference(set(team_groups['new_name']))
    return input_data.drop(columns=dropped_cols)

def generate_new_models(input_data_filepath, team_groups_filepath=None):
    """
        Generates model models and saves them in the models folder
    """
    input_data = pd.read_excel(input_data_filepath)
    original_input_cols = list(input_data.columns)

    if team_groups_filepath:
        team_groups = pd.read_excel(team_groups_filepath)
        input_data = relabel_input_data_columns(input_data, team_groups)

    # rename columns for processing
    input_data = input_data.rename(columns = {
        "project_name": "title",
        "description": "content",
    })

    columns = input_data.columns.tolist()
    teams = columns[columns.index('NESTA')+1:]

    # Save team names
    with open(models_folder / 'team_labels.csv', 'w') as file:
        for team in teams: file.write(team + '\n')

    ### Clear out old models
    remove_old_models()

    ### Create model for NESTA
    feature_matrix = create_feature_matrix(input_data)
    labels = input_data['NESTA']

    X_train, X_test, y_train, y_test = train_test_split(feature_matrix, labels, test_size = 0.33, random_state = 42)

    nesta_model = RandomForestClassifier(n_estimators = 600)
    nesta_model.fit(X_train, y_train)

    ### Store model
    joblib.dump(nesta_model, models_folder / 'nesta_model.pkl')

    ### Make a df of X and all y columns, but only for projects labelled as interesting
    team_y_df =  input_data[['NESTA'] + teams].fillna(0)

    team_model_df = pd.concat([feature_matrix, team_y_df], axis=1)
    team_model_df = team_model_df[team_model_df.NESTA==1]

    ### Give them scores & save the models
    team_output_df = pd.DataFrame()

    for team in teams:
        print('Currently on: {}'.format(team))

        # Setup
        team_y = team_model_df[team]
        team_X = team_model_df[feature_matrix.columns]
        team_X_train, team_X_test, team_y_train, team_y_test = train_test_split(team_X, team_y, test_size = 0.33, random_state = 42)

        # Make model & predictions
        team_model = RandomForestClassifier(n_estimators=600)
        team_model.fit(team_X_train,team_y_train)
        team_y_test_proba = team_model.predict_proba(team_X_test)

        # Organise predictions
        predictions_array = list(zip(team_y_test.index, team_y_test, team_y_test_proba[:,1]))
        prediction_df_col_names = ['index','true_{}'.format(team),'proba_{}'.format(team)]
        predictions_df = pd.DataFrame(predictions_array, columns=prediction_df_col_names).set_index('index')

        team_output_df = pd.concat([team_output_df,predictions_df],axis=1)

        # Store models
        team_model_name = 'team_model_{}.pkl'.format(team)
        joblib.dump(team_model, models_folder / team_model_name)


if __name__ == '__main__':
    data_folder =  Path(__file__).resolve().parent

    input_data_filepath = data_folder / 'data' / 'input_data.xlsx'
    team_groups_filepath = data_folder / 'data' / 'team_groups.xlsx'

    generate_new_models(input_data_filepath, team_groups_filepath)
