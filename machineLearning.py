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


"""
Makes a set of words, and print every word and number of the words occurences in the tweets.
"""

def wordCount( inputFile ):
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

    # Count occurences of one word. Primarily for checking that it is the right tweets imported
    word = "sport"
    print "Word \'", word,"\' occurs", wordlist.count(word), "times."

    # Print occurences for every word in vocab; And output to file 'data.txt'
    for word in vocab:
       o = wordlist.count(word)
       #print word, o
       outputFile.write(word)
       outputFile.write('\t')
       outputFile.write(str(o))
       outputFile.write('\n')

    print "Data written to output file"
       

"""
Uses tmgSimple to make e textmatrix of the input tweets
"""

def makeTextMatrix( inputFile, stopwordFile ):
    # Generate text matrix with TmgSimple from 02450
    textMatrix = TmgSimple(filename=inputFile, stopwords_filename=stopwordFile)

    X = textMatrix.get_matrix(sort=True)
    attributeNames = textMatrix.get_words(sort=True)


    # Display the result
    print attributeNames
    print X