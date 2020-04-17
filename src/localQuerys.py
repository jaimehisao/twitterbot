import tweepy

from src.config import create_api

import src.mongoer
import pymongo


def query_by_screenname(screen_name):
    mongo = src.mongoer.Mongo()
    database = mongo.return_twitter_user_tweet_collection()

    tweets = database.find({'screenName': screen_name})
    print('The user ' + str(screen_name) + ' has ' + str(tweets.count()) + ' in the database.')

    del mongo
