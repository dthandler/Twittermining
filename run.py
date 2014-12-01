# -*- coding: utf-8 -*-
"""
Collection & processing of tweets
"""

from machineLearning import MachineLearning
from tweetMining import TweetMining

"""
running tweetMining - authentication keys are needed
keys can be stored in a cfg file or hardcoded
search_tweets(hundreds of desired tweets, query string, output filename)
"""
tweetminer = TweetMining()
tweetminer.search_tweets(1, 'sport', 'data/output_test1.txt')

"""
running machineLearning
"""

# databaseFile = 'data/test40k_2nd.txt'
databaseFile = 'data/database_3900tweets.txt'
stopwordFile = 'data/stopwords.txt'

analysis = MachineLearning(databaseFile, stopwordFile)

