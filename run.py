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
tweetminer.search_tweets(400, 'sport', 'data/sport_40000tweets.txt')

"""
running machineLearning
"""

databaseFile = 'data/sport_1000tweets.txt'
stopwordFile = 'data/stopwords.txt'

analysis = MachineLearning(databaseFile, stopwordFile)

