# -*- coding: utf-8 -*-
"""
Textprocessing of tweets

Author:
Daniel Handler
s113446
Technical University of Denmark
"""

from machineLearning import MachineLearning

#databaseFile = 'data/test40k_2nd.txt'
databaseFile = 'data/database_3900tweets.txt'
stopwordFile = 'data/stopwords.txt'

analysis = MachineLearning(databaseFile, stopwordFile)

