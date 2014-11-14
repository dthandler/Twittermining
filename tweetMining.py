import twython
import re
import codecs
from twython.exceptions import TwythonError

class TweetMining:
    twitter = None

    def __init__(self, Consumer_Key, Consumer_Secret, Secret_Token=None):
        """
        Application-only authentication to twitter.
        Authenticates with a token, use keys if there is none.
        """
        if Secret_Token != None:
            self.twitter = twython.Twython(Consumer_Key, access_token=Secret_Token)
        else:
            self.twitter = twython.Twython(Consumer_Key, Consumer_Secret, oauth_version=2)
            Secret_Token = TweetMining.twitter.obtain_access_token()
            print('Your access token is: ', Secret_Token)
     
    def save_tweets(self, search_statuses, filename):
        """
        Save a list of tweet in a text file from a list of statuses
        """
        status_texts = [ status['text'] for status in search_statuses ]
        with codecs.open(filename, 'a', encoding="utf-8") as f:
            f.write(";\n".join(status_texts))
    
    def next_search_id(self, search_next_results):
        """
        Return the max_id needed to continue a search. 
        """
        return re.findall('\d+', search_next_results)[0]
    
    def search_iteration(self, search_query, filename, search_max_id=None):
        """
        Execute a 100 tweet iteration of a search, write the results and return
        the max_id for the next search
        """
        if search_max_id != None:
            query = dict(q=search_query, max_id=search_max_id, lang='en', result_type='recent', count=100)
        else:
            query = dict(q=search_query, lang='en', result_type='recent', count=100)
        try:
            tweet_search = self.twitter.search(**query)
        except TwythonError:
            print("Problem with Twython")
        tweet_statuses = tweet_search['statuses']
        self.save_tweets(tweet_statuses, filename)
        return self.next_search_id(tweet_search['search_metadata']['next_results'])
    
    def search_tweets(self, search_count, search_query, filename):
        """
        Search tweets, deals with the limited count of the queries
        """
        max_id = None
        for i in range(0, search_count):
            max_id = self.search_iteration(search_query, filename, max_id)
            print("Iteration ", i+1, " of ", search_count, " done.")
