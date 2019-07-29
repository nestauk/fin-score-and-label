import json
import numpy as np
import pytest
from sklearn.ensemble.forest import RandomForestClassifier
from nesta_score_label.nesta_score_label import *

@pytest.fixture
def mocked_keywords():
    return ['one', 'two', 'three', 'four']

@pytest.fixture
def mocked_entry():
    return {
        'title': 'one bag of carrots',
        'content': 'is one, two or three enough?'
    }

@pytest.fixture
def real_keywords():
    with open('./nesta_score_label/models/saved_keywords.csv') as file:
        keywords = [w for w in file.read().split('\n')[1:] if len(w) > 0]
    return keywords

@pytest.fixture
def team_names():
    return [
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

def test_successful_feature_matrix_created(mocked_entry, mocked_keywords):
    mocked_entries = [mocked_entry]
    fm = create_feature_matrix(mocked_entries, mocked_keywords)

    column_names = fm.columns.tolist()
    project_name_columns = [c for c in column_names if "project_name" in c]
    description_columns = [c for c in column_names if "description" in c]

    # check all correct columns
    assert len(project_name_columns) == len(mocked_keywords) + 2
    assert len(description_columns) == len(mocked_keywords) + 2

    # check correct num rows
    assert fm.shape[0] == 1

    # check correct data
    assert fm.iloc[0].total_project_name_clean_count == 1
    assert fm.iloc[0]['project_name_clean_count_%_keywords'] == 0.25
    assert fm.iloc[0].total_description_clean_count == 3
    assert fm.iloc[0]['description_clean_count_%_keywords'] == 0.5

def test_successful_calculate_scores_created(mocked_entry, real_keywords):
    mocked_entries = [mocked_entry]
    fm = create_feature_matrix(mocked_entries, real_keywords)

    scores = calculate_scores(fm)

    # check the size of the output is correct
    assert scores.shape[0] == len(mocked_entries)

def test_successful_calculate_labels_created(mocked_entry, real_keywords):
    mocked_entries = [mocked_entry]
    fm = create_feature_matrix(mocked_entries, real_keywords)

    labels = calculate_labels(fm)

    # check the size of the output is correct
    assert labels.shape[0] == len(mocked_entries)

def test_load_model(team_names):
    nesta_model = load_model("nesta_model.pkl")
    assert type(nesta_model) == RandomForestClassifier

    for name in team_names:
        model = load_model("team_model_" + name + ".pkl")
        assert type(model) == RandomForestClassifier

def test_load_keywords(real_keywords):
    keywords = load_keywords()
    assert len(keywords) == len(real_keywords)
    assert set(keywords) == set(real_keywords)

def test_len_tokenized_text():
    l = len_tokenized_text("this is a great set of words")
    assert l == 7

def test_get_counting_cols():

    df = pd.DataFrame({
        'text': ['this is a list of keywords where keywords are good'],
    })

    keywords = ['keywords', 'list']

    x = get_counting_cols(df, 'text', keywords)

    assert set(x.columns.tolist()) == set(['text_count_' + s for s in keywords])
    assert x.iloc[0].text_count_keywords == 2
    assert x.iloc[0].text_count_list == 1

def test_tidy_text():
    text = "WHERE IS the 1 THING\n\r\n THAT I NEED!!!!!"
    ttext = tidy_text(text)
    assert ttext == "where is the 1 thing   that i need"

def test_binary_cols_to_concat_text(team_names):

    pred_teams = ['pred_' + s for s in team_names]

    df = pd.DataFrame({team: [1] for team in pred_teams})

    label = binary_cols_to_concat_text(df.iloc[0], pred_teams, team_names)

    assert label == ', '.join(teams)
