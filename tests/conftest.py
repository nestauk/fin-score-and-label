import pytest
import os
import shutil
from pathlib import Path
from nesta_score_label.generate_models import generate_new_models

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

@pytest.fixture
def generate_test_models():
    def func():
        test_models_path = Path(__file__).resolve().parent / 'models'
        try:
            os.mkdir(test_models_path)
        except FileExistsError as e:
            pass

        input_data_filepath = Path(__file__).resolve().parent / 'input_data_test.xlsx'
        generate_new_models(input_data_filepath, models_folder=test_models_path)
    return func

@pytest.fixture
def remove_test_models():
    def func():
        test_models_path = Path(__file__).resolve().parent / 'models'
        shutil.rmtree(test_models_path)
    return func
