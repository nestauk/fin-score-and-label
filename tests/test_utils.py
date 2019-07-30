import pandas as pd
from sklearn.ensemble.forest import RandomForestClassifier
from nesta_score_label.utils import *

def test_load_model(generate_test_models, remove_test_models):
    generate_test_models()
    test_models_path = Path(__file__).resolve().parent / 'models'
    nesta_model = load_model("nesta_model.pkl", test_models_path)
    assert type(nesta_model) == RandomForestClassifier

    teams = load_teams(test_models_path)

    for name in teams:
        model = load_model("team_model_" + name + ".pkl", test_models_path)
        assert type(model) == RandomForestClassifier
    remove_test_models()

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

    assert label == ', '.join(team_names)
