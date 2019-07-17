import json
import numpy as np
import pytest
from sklearn.dummy import DummyClassifier
from nesta_score_label.nesta_score_label import create_feature_matrix, calculate_scores, calculate_labels

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
