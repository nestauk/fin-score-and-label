import json
import numpy as np
import pytest
from nesta_score_label.calculate_results import *
from nesta_score_label.utils import *

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