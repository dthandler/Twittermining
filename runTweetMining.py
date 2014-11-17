from tweetMining import TweetMining
"""
testing tweetMining - authentication keys are needed
keys can be stored in a cfg file or hardcoded
"""
tweetminer = TweetMining()

# search_tweets(hundreds of desired tweets, query string, output filename)
tweetminer.search_tweets(2, 'sport', 'output.txt')
