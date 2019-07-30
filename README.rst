==================
fin-score-and-label
==================

Basic Commands
--------------

Pre-requisites
^^^^^^^^^^^^^^
* Python3.6
* Docker

Installation and setup
^^^^^^^^^^^^^^^^^^^^^^
* Clone the current git repo
* Install python dependencies in your virtual env::

    $ pip install -r requirements.txt
    $ pip install .


Create Keywords
^^^^^^^^^^^^^^^^^^^^^^
* Create a list of unique keywords from the input file, and store it as nesta_score_label/models/saved_keywords.csv

    $ python nesta_score_label/generate_keywords.py

Generate new models
^^^^^^^^^^^^^^^^^^^^^^
* Generate predictive models for the overall nesta score and each of the team scores, and saves them in the models folder


    $ python nesta_score_label/generate_models.py

Manually editing keywords
^^^^^^^^^^^^^^^^^^^^^^
* After manually editing keywords in `nesta_score_label/models/saved_keywords.csv`, you need to generate new models
