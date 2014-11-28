************************************
TWITTER MINING USING PYTHON
************************************
NOVEMEBER-DECEMBER 2014
----------------------------
Daniel Tolboe Handler & Arthur Desjardins
Technical University of Denmark
----------------------------

************************************
I :: THE PROJECT
************************************
The microblogging platform Twitter is widely used to share opinions. Users exchange on various topics and discuss different ideas.
These tweets present a huge amount of information available for data mining.
Using data mining techniques and multivariate analysis it is possible to retrieve and analyse tweets to understand the current popular topics among the users.
This report study the identification of related topics in tweets about a given subject.
For instance, when users write tweets about sport what other topics do they talk about?

************************************
II :: PYTHON FILE LIST
************************************
machineLearning.py			The machine learning methods, including bag-of-words representation and non-negative matrix factorization
tweetMining.py				The mining methods
runTweetMining.py			Run file for the mining methods
run.py						Run file for the machine learning methods
tmgsimple.py				Tools used in machine learning methods

************************************
III :: DATABASE
************************************
The database is located in the folder 'data'.
Files with postfix .data is the bag-of-words files.
Files with postfix .txt is the tweet databases.

************************************
IV :: EXECUTION
************************************
The project is run from the two run files. The execution of runTweetMining will save a database of tweets.
The execution of run will represent them in the bag-of-words, and calculate the matrix factorization.