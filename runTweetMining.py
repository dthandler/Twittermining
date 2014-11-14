from tweetMining import TweetMining

#testing tweetMining

APP_KEY = ''
APP_SECRET = ''
ACCESS_TOKEN = ''

#Access token is optional

tweetminer = TweetMining(APP_KEY,APP_SECRET,ACCESS_TOKEN)

# search_tweets(hundreds of tweets desired int, query string, output filename string)
tweetminer.search_tweets(2, 'sport', 'output.txt')



