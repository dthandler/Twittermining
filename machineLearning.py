"""
Textprocessing of tweets

Author:
Daniel Handler
s113446
Technical University of Denmark

Disclaimer: TmgSimple package from course
02450 Introduction to Machine Learning
"""


import numpy as np
from tmgsimple import TmgSimple
from sklearn.decomposition import ProjectedGradientNMF
import nltk
import re

"""
GLOBAL VARIABLES
"""
attributFile = 'data/attributes.data'
dataFile = 'data/datamatrix.data'
formattedDatabase = "data/formattedDatabase.data"


class MachineLearning:

    def __init__(self, databaseFile, stopwordFile):
        self._formatDatabase(databaseFile)
        self._makeTextMatrix(databaseFile, stopwordFile)

        self._nonNegativeFactorization()

    """
    Uses tmgSimple to make e textmatrix of the input tweets
    """

    def _formatDatabase(self, dataBase):
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
            attFile.write(str(word, '\n'))

        for i in range(40):
            np.savetxt(datFile, textMatrix.get_matrix(i*1000, (i+1)*1000,
                                                      sort=True), fmt='%i')

    """
    Uses sklearn to make the non negative factorization
    """

    def _nonNegativeFactorization(self):

        print 'Loading data..'
        X = np.asmatrix(np.loadtxt(dataFile))
        print 'Data loaded. Making model..'
        model = ProjectedGradientNMF(init='nndsvd')
        print 'Fitting model..'
        model.fit(X)
        print 'Model fit'

    """
    THE FOLLOWING IS A SMALL COLLECTION OF MACHINE LEARNING METHODS;
    THESE ARE DEVELOPED TO CHECK THE IMPLEMENTATION OF THE
    BAG OF WORD REPRESENTATION AND THE MATRIX FACTORIZATION
    """

    """
    Makes a set of words. Print every word
    and number of the words occurences in the tweets.
    If second argument is used
    the method prints the number of occurences of the given word.
    """

    def wordCount(self, inputFile, inputWord=0):
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

    """
    Print out a sorted list of word from a given tweet
    """

    def getWordsFromTweet(self, tweetNo):
        X = np.asmatrix(np.loadtxt(dataFile))
        tweet = X.getA()[tweetNo]
        header = self._sanitizeColumnheader()

        for attributeNo, value in enumerate(tweet):
            if value != 0:
                print header[attributeNo]

    """
    Count all occurences of each word, and find the most used.
    Optimized version which uses more build-in functions than last iteration
    """

    def findMostPopularWord(self):
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

    """
    Given a list of words, the methods predicts which words
    might be in tweets with the word in the word list
    and calculates the probability that this is the case.
    """

    def assiciateMining(self, wordList):

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
