import pytest

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
