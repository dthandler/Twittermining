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
import nltk
import re

"""
GLOBAL VARIABLES
"""
attributFile = 'attributes.txt'
dataFile = 'datamatrix.txt'
formattedDatabase = "formattedDatabase.txt"


"""
Makes a set of words. Print every word
and number of the words occurences in the tweets.
If second argument is used
the method prints the number of occurences of the given word.
"""


def wordCount(inputFile, inputWord=0):
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


"""
Uses tmgSimple to make e textmatrix of the input tweets
"""


def formatDatabase(dataBase):
    f = open(dataBase)

    array = (re.compile("\n").sub(" ", f.read())).split("; ")

    outputFile = open(formattedDatabase, 'w')

    for tweet in array:
        outputFile.write(tweet)
        outputFile.write('\n')


def makeTextMatrix(inputFile, stopwordFile):

    # Format the database according to our specifications
    formatDatabase(inputFile)

    # Generate text matrix with TmgSimple from 02450
    textMatrix = TmgSimple(filename=formattedDatabase,
                           stopwords_filename=stopwordFile)

    X = textMatrix.get_matrix(sort=True)
    attributeNames = textMatrix.get_words(sort=True)

    # Make an output file
    outputFile = open(attributFile, 'w')

    for word in attributeNames:
        outputFile.write(word)
        outputFile.write('\n')

    np.savetxt(dataFile, X, fmt='%i')


"""
Print out a sorted list of word from a given tweet
"""


def getWordsFromTweet(tweetNo):
    X = np.asmatrix(np.loadtxt(dataFile))
    tweet = X.getA()[tweetNo]
    header = sanitizeColumnheader()

    for attributeNo, value in enumerate(tweet):
        if value != 0:
            print header[attributeNo]


"""
Count all occurences of each word, and find the most used.
This version is optimized and uses more build-in functions than last iteration
"""


def findMostPopularWord():
    # Import the tweets and list the raw words
    raw = open(formattedDatabase).read()
    rawWordlist = [word.lower() for word in nltk.word_tokenize(raw)]

    # Get all words
    wordlist = sanitizeColumnheader()

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
Count all occurences of each word, and find the k most used. K is 3 as standard
"""


def findKMostPopularWords(K=3):
    X = np.asmatrix(np.loadtxt(dataFile))

    header = sanitizeColumnheader()

    maxList = []

    for k in range(K):
        maxList.append((0, 0))

    currentMinMax = 0
    minMaxIndex = 0
    currentCounter = 0

    for wordID, word in enumerate(header):
        currentCounter = 0
        for tweet in range(len(X[:, wordID])):
            currentCounter += X[tweet, wordID]

        if currentCounter > currentMinMax:
            maxList[minMaxIndex] = (currentCounter, word)
            minMaxIndex = findNewMinMax(maxList)

    print maxList

# Finds the lowest tuppelvalue in a list of tuples.
# Used in findKMostPopularWords()-method


def findNewMinMax(tuppelList):
    currentMin = 1000
    minIndex = 0
    for no, (x, y) in enumerate(tuppelList):
        if x < currentMin:
            currentMin = x
            minIndex = no
    return minIndex


# Sanitize columnheader
def sanitizeColumnheader():
    y = open(attributFile, 'r').readlines()
    header = []

    for line in y:
        header.append(re.sub("\n", "", line))

    return np.asarray(header)

"""
Given a list of words, the methods predicts which words
might be in tweets with the word in the word list
and calculates the probability that this is the case.
"""


def assiciateMining(wordList):

    # Initialisation of variables
    noOfWords = len(wordList)

    X = np.asmatrix(np.loadtxt(dataFile))
    header = sanitizeColumnheader()

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
        # If this is true, all words in wordList is in the current tweet
            predicting = predicting + row
            similarTweets = similarTweets + 1

    for index in indexes:  # Removing the searchword from the result vector
        predicting[index] = 0

    for index, occurence in enumerate(predicting):
    # Calc. probability for occurence for each word, and saves them in a list
        if occurence > 0:
            probability = (occurence / similarTweets) * 100
            outputList.append((header[index], probability))

    # Prints result
    print outputList
