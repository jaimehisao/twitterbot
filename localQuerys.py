import tweepy

from config import create_api

import mongoer
import pymongo

def queryByScreenName(screenName):
    mongo = mongoer.Mongo()
    database = mongo.returnTwitterUserTweetsCollection()

    tweets = database.find({'screenName' :screenName})
    print('The user ' + str(screenName) + ' has ' + str(tweets.count()) + ' in the database.')

    del mongo

