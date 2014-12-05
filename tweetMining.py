# -*- coding: utf-8 -*-
"""
Collection of tweets

Author:
Arthur Desjardins
s131187
Technical University of Denmark
"""

import twython
import os
import re
import codecs
import configparser


class TweetMining:
    twitter = None

    def __init__(self, Consumer_Key=None, Consumer_Secret=None,
                 Secret_Token=None):
        """
        Application-only authentication to twitter.
        Authenticates with a token, use keys if there is none.
        By default look for a cfg file, credentials can also
        be given as arguments.
        """
        if os.path.isfile('app.cfg'):
            config = configparser.RawConfigParser()
            config.read('app.cfg')
            Consumer_Key = config.get('twitter', 'APP_KEY')
            Consumer_Secret = config.get('twitter', 'APP_SECRET')
            Secret_Token = config.get('twitter', 'ACCESS_TOKEN')
        if (Secret_Token is not None and Consumer_Key is not None and
                Consumer_Secret is not None):
            self.twitter = twython.Twython(Consumer_Key,
                                           access_token=Secret_Token)
        elif (Secret_Token is None and Consumer_Key is not None and
                Consumer_Secret is not None):
            self.twitter = twython.Twython(Consumer_Key, Consumer_Secret,
                                           oauth_version=2)
            Secret_Token = TweetMining.twitter.obtain_access_token()
            print('Your access token is: ', Secret_Token)
        elif (Consumer_Key is None or Consumer_Secret is None):
            print("Twitter authentication error, please use a cfg file")

    def _save_tweets(self, search_statuses, filename):
        """
        Save a list of tweet in a text file from a list of statuses
        """
        status_texts = [status['text'] for status in search_statuses]
        with codecs.open(filename, 'a', encoding="utf-8") as f:
            f.write(";\n".join(status_texts))

    def _next_search_id(self, search_next_results):
        """
        Return the max_id needed to continue a search.
        """
        return re.findall('\d+', search_next_results)[0]

    def _search_iteration(self, search_query, filename, search_max_id=None):
        """
        Execute a 100 tweet iteration of a search, write the results and return
        the max_id for the next search
        """
        if search_max_id is not None:
            query = dict(q=search_query, max_id=search_max_id, lang='en',
                         result_type='recent', count=100)
        else:
            query = dict(q=search_query, lang='en', result_type='recent',
                         count=100)
        try:
            tweet_search = self.twitter.search(**query)
            tweet_statuses = tweet_search['statuses']
            self._save_tweets(tweet_statuses, filename)
            return self._next_search_id(tweet_search['search_metadata']
                                        ['next_results'])
        except AttributeError:
            print("Problem with the authentication, please enter credentials")

    def search_tweets(self, search_count, search_query, filename):
        """
        Search tweets, deals with the limited count of the queries
        """
        max_id = None
        for i in range(0, search_count):
            max_id = self._search_iteration(search_query, filename, max_id)
            print("Iteration ", i + 1, " of ", search_count, " done.")
