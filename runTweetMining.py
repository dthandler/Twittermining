from tweetMining import TweetMining

#testing tweetMining - authentication keys are needed, they can be in a cfg file
tweetminer = TweetMining()

# search_tweets(hundreds of desired tweets, query string, output filename)
tweetminer.search_tweets(2, 'sport', 'test_l.txt')
