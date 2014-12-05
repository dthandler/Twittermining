# -*- coding: utf-8 -*-
"""
Textprocessing of tweets

Disclaimer: TmgSimple % toolbox_02450 packages from course
02450 Introduction to Machine Learning
"""

import numpy as np
from tmgsimple import TmgSimple
from sklearn.decomposition import ProjectedGradientNMF
from sklearn.cluster import k_means
from pylab import figure, show
from toolbox_02450 import clusterplot
import nltk
import re

"""
GLOBAL VARIABLES
"""
attributFile = 'data/attributes.data'
dataFile = 'data/datamatrix.data'
formattedDatabase = 'data/formattedDatabase.data'
factoredHMatrix = 'data/factoredHMatrix.data'
factoredWMatrix = 'data/factoredWMatrix.data'


class MachineLearning:

    def __init__(self, databaseFile, stopwordFile):
        self._formatDatabase(databaseFile)
        self._makeTextMatrix(databaseFile, stopwordFile)
        # self._nonNegativeFactorization()
        # self._clustering()
        self._nmf_with_results(10)

    def _formatDatabase(self, dataBase):
        """
        Uses tmgSimple to make e textmatrix of the input tweets
        """

        f = open(dataBase)

        array = (re.compile("\n").sub(" ", f.read())).split("; ")

        outputFile = open(formattedDatabase, 'w')

        for tweet in array:
            outputFile.write(tweet)
            outputFile.write('\n')

    def _makeTextMatrix(self, inputFile, stopwordFile):

        # Generate text matrix with TmgSimple from 02450
        textMatrix = TmgSimple(filename=formattedDatabase,
                               stopwords_filename=stopwordFile)

        attributeNames = textMatrix.get_words(sort=True)

        # Make an output file
        attFile = open(attributFile, 'w')
        datFile = open(dataFile, 'w')

        for word in attributeNames:
            attFile.write(word)
            attFile.write('\n')

        attFile.close

        for i in range(40):
            np.savetxt(datFile, textMatrix.get_matrix(i*1000, (i+1)*1000,
                                                      sort=True), fmt='%i')
        datFile.close

    def _nonNegativeFactorization(self):
        """
        Uses sklearn to make the non negative factorization
        """

        print 'Loading data..'
        X = np.asmatrix(np.loadtxt(dataFile))
        print 'Data loaded. Making model..'
        model = ProjectedGradientNMF(init='nndsvd')
        print 'Fitting model..'
        model.fit(X)
        print 'Model fit'

        print 'Error rate is', model.reconstruction_err_

        #  H-matrix
        outFile1 = open(factoredHMatrix, 'w')
        np.savetxt(outFile1, model.components_, fmt='%i')
        outFile1.close

        # W-matrix
        outFile2 = open(factoredWMatrix, 'w')
        np.savetxt(outFile2, model.transform(X), fmt='%i')
        outFile2.close

    def _nmf_with_results(self, k):
        """
        Encapsulate the NMF runs
        Print the results as plain text
        input: k, max number of clusters
        author: Arthur Desjardins
        """
        X = np.asmatrix(np.loadtxt(dataFile))
        for i in range(0, k):
            print i+1, 'clusters:', self._nmf_fixed_component(i+1, X)

    def _nmf_fixed_component(self, i, X):
        """
        Uses sklearn to make the non negative factorization
        input: i, number of clusters for this NMF instance
        author: Arthur Desjardins
        """
        model = ProjectedGradientNMF(n_components=i, init='nndsvd')
        model.fit(X)
        #  H-matrix (clusters x words)
        H = model.components_
        # W-matrix (documents x clusters)
        W = model.transform(X)
        # word matrix
        words = open(attributFile).read().split()
        # processing extremely basic cluster bush
        most_relevant_words = np.argmax(H, axis=1)
        docs_per_cluster = [0]*i
        for tweet in W:
            most_relevant_cluster = np.argmax(tweet)
            docs_per_cluster[most_relevant_cluster] += 1
        clusters = dict(((words[most_relevant_words[i]], docs_per_cluster[i])
                         for i in range(0, i)))
        return clusters

    def _clustering(self):

        # Get data
        print 'Get cluster data..'
        H = np.asmatrix(np.loadtxt(factoredHMatrix)).T
        words = set(open(attributFile).read().split())

        y = range(len(words))

        # clustering
        clusterNumber = 4
        runNumber = 10
        N, M = H.shape

        print 'Calculate k-means..'
        # K-means clustering:
        centroids, cls, inertia = k_means(H, clusterNumber, n_init=runNumber)
        print 'Plotting results..'
        # Plot results:
        figure(figsize=(14, 9))
        clusterplot(H, cls, centroids, y)
        show()

    """
    THE FOLLOWING IS A SMALL COLLECTION OF MACHINE LEARNING METHODS;
    THESE ARE DEVELOPED TO TEST THE IMPLEMENTATION OF THE
    BAG OF WORD REPRESENTATION AND THE MATRIX FACTORIZATION
    """

    def wordCount(self, inputFile, inputWord=0):
        """
        Makes a set of words. Print every word
        and number of the words occurences in the tweets.
        If second argument is used
        the method prints the number of occurences of the given word.
        """
        # Import the tweets
        raw = open(inputFile).read()

        # List the words
        wordlist = [w.lower() for w in nltk.word_tokenize(raw)]

        # Make a sorted set of the words
        vocab = sorted(set(wordlist))

        if inputWord == 0:
            # Make an output file
            outputFile = open('data.txt', 'w')
            # Print occurences for every word in vocab;
            # And output to file 'data.txt'
            for word in vocab:
                o = wordlist.count(word)
                outputFile.write(word)
                outputFile.write('\t')
                outputFile.write(str(o))
                outputFile.write('\n')

            print "Data written to output file"

        else:
            print inputWord, 'has', wordlist.count(inputWord), 'occurences'

    # Sanitize columnheader
    def _sanitizeColumnheader(self):
        y = open(attributFile, 'r').readlines()
        header = []

        for line in y:
            header.append(re.sub("\n", "", line))

        return np.asarray(header)

    def getWordsFromTweet(self, tweetNo):
        """
        Print out a sorted list of word from a given tweet
        """
        X = np.asmatrix(np.loadtxt(dataFile))
        tweet = X.getA()[tweetNo]
        header = self._sanitizeColumnheader()

        for attributeNo, value in enumerate(tweet):
            if value != 0:
                print header[attributeNo]

    def findMostPopularWord(self):
        """
        Count all occurences of each word, and find the most used.
        Optimized version: Uses more build-in functions than last iteration
        """
        # Import the tweets and list the raw words
        raw = open(formattedDatabase).read()
        rawWordlist = [word.lower() for word in nltk.word_tokenize(raw)]

        # Get all words
        wordlist = self._sanitizeColumnheader()

        currentMax = 0
        currentWord = 'none'
        occurences = 0

        for word in wordlist:
            occurences = rawWordlist.count(word)  # To minimize calculations
            if occurences > currentMax:
                currentMax = occurences
                currentWord = word

        print currentWord, 'has', currentMax, 'occurences'

    def assiciateMining(self, wordList):
        """
        Given a list of words, the methods predicts which words
        might be in tweets with the word in the word list
        and calculates the probability that this is the case.
        """

        # Initialisation of variables
        noOfWords = len(wordList)

        X = np.asmatrix(np.loadtxt(dataFile))
        header = self._sanitizeColumnheader()

        vector = [0 for x in range(len(header))]
        predicting = [0 for x in range(len(header))]

        outputList = []

        # Defining the vector to compare
        for word in wordList:
            if word in header:
                x = np.where(header == word)[0][0]
                vector[x] = 1

        indexes = [i for i, j in enumerate(vector) if j == 1]

        similarTweets = 0  # Counter variable

        for row in X:
            similarityCounter = 0
            row = row.getA()[0]

            for index in indexes:
                if row[index] == 1:
                    similarityCounter = similarityCounter + 1

            if similarityCounter == noOfWords:
                # If true, all words in wordList is in the current tweet
                predicting = predicting + row
                similarTweets = similarTweets + 1

        for index in indexes:  # Removing the searchword from resultvector
            predicting[index] = 0

        for index, occurence in enumerate(predicting):
            # Calc. prob. for occ. for each word, and saves them in a list
            if occurence > 0:
                probability = (occurence / similarTweets) * 100
                outputList.append((header[index], probability))

        # Prints result
        print outputList
