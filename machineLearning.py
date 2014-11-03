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

# Import the tweets
f = open('database.txt')
raw = f.read()

# List the words
wordlist = [w.lower() for w in nltk.word_tokenize(raw)]

# Make a sorted set of the words
vocab = sorted(set(wordlist))

# Print the set of words
print vocab

# Count occurences of one word
word = "Sport"
print wordlist.count(word)

# Print occurences for every word in vocab
for word in vocab:
    o = wordlist.count(word)
    print word, o





"""
# Generate text matrix with TmgSimple from 02450
textMatrix = TmgSimple(filename='testDatabase.txt', stopwords_filename='stopwords.txt')

X = textMatrix.get_matrix(sort=True)
attributeNames = textMatrix.get_words(sort=True)


# Display the result
print attributeNames
print X
"""