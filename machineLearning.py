"""
Textprocessing of tweets

Author:
Daniel Handler
s113446
Technical University of Denmark

Disclaimer: TmgSimple package from course 02450 Introduction to Machine Learning
"""


import numpy as np
from tmgsimple import TmgSimple
import nltk
import re


"""
Makes a set of words, and print every word and number of the words occurences in the tweets.
If second argument is used, the method prints the number of occurences of the given word.
"""

def wordCount( inputFile , inputWord=0):
    # Import the tweets
    raw = open(inputFile).read()

    # List the words
    wordlist = [w.lower() for w in nltk.word_tokenize(raw)]

    # Make a sorted set of the words
    vocab = sorted(set(wordlist))

    # Print the set of words
    #print vocab

    # Make an output file
    outputFile = open('data.txt', 'w')


    if inputWord == 0:    
        # Print occurences for every word in vocab; And output to file 'data.txt'
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
def makeTextMatrix( inputFile, stopwordFile ):
    # Generate text matrix with TmgSimple from 02450
    textMatrix = TmgSimple(filename=inputFile, stopwords_filename=stopwordFile)

    X = textMatrix.get_matrix(sort=True)
    attributeNames = textMatrix.get_words(sort=True)

    # Make an output file
    outputFile = open('attributes.txt', 'w')
    
    for word in attributeNames:        
        outputFile.write(word)
        outputFile.write('\n')
        
    np.savetxt('datamatrix.txt', X, fmt='%i')


"""
Print out a sorted list of word from a given tweet
"""     
def getWordsFromTweet( tweetNo ):
    X = np.asmatrix(np.loadtxt('datamatrix.txt'))
    tweet = X.getA()[tweetNo]
    header = sanitizeColumnheader()
    
    for attributeNo, value in enumerate(tweet):
        if value != 0:
            print header[attributeNo]


"""
Count all occurences of each word, and find the most used
"""
def findMostPopularWord():
    X = np.asmatrix(np.loadtxt('datamatrix.txt'))
    
    header = sanitizeColumnheader()
    
    currentMax = 0
    currentCounter = 0
    currentWord = 'none'
    
    for wordID, word in enumerate(header):
        currentCounter = 0
        for tweet in range(len(X[:,wordID])):
            currentCounter += X[tweet,wordID]

        if currentCounter > currentMax:
            currentMax = currentCounter
            currentWord = word
    
    print currentWord, currentMax
    
"""
Count all occurences of each word, and find the k most used. K is 3 as standard
"""
def findKMostPopularWords( K = 3 ):
    X = np.asmatrix(np.loadtxt('datamatrix.txt'))
    
    header = sanitizeColumnheader()
    
    maxList = []
    
    for k in range(K):
        maxList.append((0,0))
        
    currentMinMax = 0
    minMaxIndex = 0
    currentCounter = 0
    
    
    
    for wordID, word in enumerate(header):
        currentCounter = 0
        for tweet in range(len(X[:,wordID])):
            currentCounter += X[tweet,wordID]

        if currentCounter > currentMinMax:
            maxList[minMaxIndex] = (currentCounter, word)
            minMaxIndex = findNewMinMax(maxList)
                
    print maxList

#Finds the lowest tuppelvalue in a list of tuples. Used in findKMostPopularWords()-method
def findNewMinMax( tuppelList ):
    currentMin = 1000
    minIndex = 0
    for no,(x,y) in enumerate(tuppelList):
        if x < currentMin:
            currentMin = x
            minIndex = no
    return minIndex
    
#Sanitize columnheader
def sanitizeColumnheader():
    y = open('attributes.txt','r').readlines()
    header = []
    
    # Sanitize columnheader
    for line in y:
        header.append(re.sub("\n","",line))
    
    return np.asarray(header)

"""
Given a list of words, the methods predicts which words might be in tweets with the word in the word list
and calculates the probability that this is the case.
"""
def predictWord( wordList ):
    
    #Initialisation of variables
    noOfWords = len(wordList)
    
    X = np.asmatrix(np.loadtxt('datamatrix.txt'))    
    header = sanitizeColumnheader()
    
    vector = [0 for x in range(len(header))]
    predicting = [0 for x in range(len(header))]
    
    outputList = []
    
    #Defining the vector to compare
    for word in wordList:
        if word in header:
            x = np.where(header==word)[0][0]
            vector[x] = 1
            
    indexes = [i for i,j in enumerate(vector) if j == 1]

    similarTweets = 0 #Counter variable

    for row in X:
        similarityCounter = 0
        row = row.getA()[0]
        
        for index in indexes:
            if row[index] == 1:
                similarityCounter = similarityCounter + 1
        
        if similarityCounter == noOfWords: #If this is true, all words in wordList is in the current tweet
            predicting = predicting + row
            similarTweets = similarTweets + 1
    
    for index in indexes: #Removing the searchword from the result vector
        predicting[index] = 0
    
    for index, occurence in enumerate(predicting): #Calculating probability for occurence for each word, and saves them in a list
        if occurence > 0:
            probability = (occurence / similarTweets) * 100
            outputList.append((header[index], probability))

    #Prints result
    print outputList