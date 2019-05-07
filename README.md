# DataAnalysisCapstone


We collected 50,500 comments and replies from 19 Reddit posts from various subreddits such as r/liberal, r/politics, r/conservative, r/the_donald, r/Republican, r/neutral_politics, r/conspiracy, etc. This data was stored into a json file called "final_indico.json" which was augmented with sentiment and political compass scores from the Indico API (https://indico.io/docs/).

Sentiment Analysis - Allows user to find sentiment of either a particluar post or of the subreddit as a whole. Further instructions within Jupyter notebook.

Team members: Chris Blair, Bright Zheng, Numan Khan, Sourav Panth

Chris: Mental Health

Bright: ./data, ./data_collection, ./ldamodels, ./topic_modelling

Numan: Sentiment Analysis

Sourav: Sentiment Analysis

# Directions In order to run the notebooks 

1. Ensure you have python 3, open a terminal and run python --version

Mine returned 
$ python --version
Python 3.7.3

2. Clone the repo and open it in a terminal 

3. Ensure you have pip installed, open a terminal and run pip --version

Mine Returned

$ pip --version

pip 19.0.3 from ~\programs\python\python37\lib\site-packages\pip (python 3.7)

4. Run pip install -r requirements.txt

5. Clear up any dependency issues, as well as, get an API key from Indico API (https://indico.io/docs/)

6. Place the indico API key as a variable named indico.config.apikey in the notebook

7. You can now run the notebooks
