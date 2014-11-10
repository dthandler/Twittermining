"""
Textprocessing of tweets

Author:
Daniel Handler
s113446
Technical University of Denmark
"""

import machineLearning as ml

databaseFile = 'database.txt'
stopwordFile = 'stopwords.txt'

#ml.wordCount(databaseFile, inputWord='liverpool')
#ml.makeTextMatrix(databaseFile, stopwordFile)

#ml.getWordsFromTweet(79)
#ml.findMostPopularWord()

#ml.findKMostPopularWords(K=6)

ml.predictWord(['football','everton'])