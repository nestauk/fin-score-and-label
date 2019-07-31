==================
fin-score-and-label
==================

Basic Commands
--------------

Pre-requisites
^^^^^^^^^^^^^^
* Python3.6

Installation and setup
^^^^^^^^^^^^^^^^^^^^^^
* Clone the current git repo
* Install python dependencies in your virtual env::

    $ pip install -r requirements.txt
    $ pip install .


Create Keywords
^^^^^^^^^^^^^^^^^^^^^^
* Create a list of unique keywords from the input file, and store it as `nesta_score_label/models/saved_keywords.csv`

    $ python nesta_score_label/generate_keywords.py

Generate new models
^^^^^^^^^^^^^^^^^^^^^^
* Generate predictive models for the overall nesta score and each of the team scores, and saves them in the models folder
* By adding `load_keywords`, the script will load the keywords from `nesta_score_label/models/saved_keywords.csv`,
* else a new set of keywords will be generated

    $ python nesta_score_label/generate_models.py [load_keywords]


Manually editing keywords
^^^^^^^^^^^^^^^^^^^^^^
* After manually editing keywords in `nesta_score_label/models/saved_keywords.csv`, you need to generate new models


How the algorithm works
^^^^^^^^^^^^^^^^^^^^^^

Prepare

	1. Input the data: Get text for each project
		* Each row of input_data.xlsx corresponds to a project (either a proposal or call for proposal), collated from multiple sources
			- Interesting calls for proposals from European Commission, taken from:
				  H2020 - Information and Communication Technologies
				  H2020 - Europe in a changing world
			- Proposals submitted by Nesta (as collated by Joana)
			- FiNN extract
				  EcEuropaDataSource
				  UKContractDataSource
				  USContractDataSource
		* Each row contains the two key text fields: project_name, project_description

	2. Label them: Is the project interesting to Nesta and each of the teams?
		* NESTA column: Nesta assign a 1 or 0 based on if it interesting to Nesta or not
		* A column for each team: Nesta assign a 1 or 0 based on if it interesting to that team or not

	3. Add keywords: Record the keywords for interesting projects
		* Keywords taken directly from proposals are added in the 'doc_keywords' column
		* Additional relevant keywords for interesting projects are manually input the 'input_keywords' column
		* Unique keywords are kept

Model

	1. Create features: Adding data points for each project
		  A:  number of times the keyword is found within project_name (for each keyword)
		  B:  number of times the keyword is found within project_description (for each keyword)
		  C:  total times keywords are found within project_name
		  D:  total time keywords are found within project_description
		  E:  C / number of characters in the project_name
		  F:  D / number of characters in the project_description

	2. Understand the model: Overview of how a Random Forest works
		* Some of the above features are selected at random, and a decision tree is created
		(e.g. It determines that If total counts of 'innovation' in the project description is above 4, the project is likely to be interesting to Nesta)
		* 600 of these decision trees are created in total, each one using a different random set of features

	3. Applying the rank: How interesting the project is to Nesta, between 0 and 1
		* A Random Forest model attempts to understand the relationship between all the features and the 'NESTA' column (interesting to Nesta vs not interesting)
		* To score a project, the output of each of these trees is recorded
		  (e.g. If 300 predict 'interesting', then the score is 300/600 = 0.5)
		* The output scores are kept as they are, in a column called 'rank'

	4. Applying the label: Identifying the teams it is interesting to
		* A different Random Forest model attempts to understand the relationship between all the features and a team column (e.g. Interesting to the CPC vs not interesting to CPC)
		* If the score for a team is >0.1, we say it is interesting to that team
		* The threshold of 0.1 was chosen because it finds correctly finds all the interesting projects for that team, and doesn't label too many that are not interesting
		* A text string is created from the team names for which the project is interesting
		* These strings are stored in a searchable column called 'label'
