"""
Textprocessing of tweets

Author:
Daniel Handler
s113446
Technical University of Denmark
"""

import machineLearning as ml

#databaseFile = 'testDatabase.txt'
databaseFile = 'database_3900tweets.txt'
stopwordFile = 'stopwords.txt'

#ml.wordCount(databaseFile, inputWord='http')
ml.makeTextMatrix(databaseFile, stopwordFile)

#ml.getWordsFromTweet(79)
ml.findMostPopularWord()

#ml.findKMostPopularWords(K=6)

#ml.assiciateMining(['football','everton'])