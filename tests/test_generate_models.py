import os
import glob
import pandas as pd
from pathlib import Path
from nesta_score_label.generate_models import *
from nesta_score_label.utils import load_teams

def test_relabel_input_data_columns():
    columns = ['source', 'group', 'code', 'project_name', 'description', 'notes', 'input_keywords', 'doc_keywords', 'NESTA', 'Innovation - Mapping', 'Innovation - NEW', 'Innovation - Digital International', 'Centre for Collective Intelligence', 'Cultural and Creative', 'CPC', 'Health Lab', 'Skills', 'Explorations', 'Education', 'Innovation - Government']
    data = pd.DataFrame({column: [1] for column in columns})

    new_teams = ["Challenge Prizes","Creative Economy (RAP and IP)","Creative Economy (RAP and IP)","Government Innovation (RAP and IP)","Government Innovation (RAP and IP)","Health Lab","Innovation Mapping","Innovation Programmes - Education","RAP Explorations","RAP Explorations","RAP Innovation","RAP Innovation","RAP Innovation","RAP Innovation","RAP Innovation","RAP Innovation","RAP International Innovation","Skills"]
    old_teams = ["CPC","Cultural and Creative","Cultural and Creative","Innovation - Government","Innovation - Government","Health Lab","Innovation - Mapping","Education","Centre for Collective Intelligence","Explorations","Innovation - NEW","Innovation - NEW","Innovation - NEW","Innovation - NEW","Innovation - NEW","Innovation - NEW","Innovation - Digital International","Skills"]

    team_groups = pd.DataFrame({
        "old_name": old_teams,
        "new_name": new_teams,
    })
    result = relabel_input_data_columns(data, team_groups)
    column_list = result.columns.tolist()
    for team in new_teams:
        assert (team in column_list)

def test_generate_new_models(generate_test_models, remove_test_models):

    generate_test_models()

    test_models_path = Path(__file__).resolve().parent / 'models'
    model_folder_contents = [os.path.basename(path) for path in glob.glob(str(test_models_path / '*'))]

    assert 'saved_keywords.csv' in model_folder_contents
    assert 'team_labels.csv' in model_folder_contents

    teams = load_teams(test_models_path)

    for team in teams:
        assert 'team_model_{}.pkl'.format(team) in model_folder_contents

    remove_test_models()
