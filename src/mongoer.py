"""
mongoer.py by Jaime Hisao Yesaki
This program connects to MongoDB and saves the tweets to the database
Created November 14, 2019
Version 0.1
"""

import pymongo


class Mongo:
    def __init__(self):
        self.mongoClient = pymongo.MongoClient("mongodb://10.0.0.4:27017/")
        self.my_db = None
        self.stats_column = None

    def __del__(self):
        self.mongoClient.close()

    # Returns Collection for listening stats
    def return_listening_stats_collection(self) -> pymongo.collection.Collection:
        self.my_db = self.mongoClient["music"]
        self.stats_column = self.my_db["listeningStats"]
        return self.stats_column

    # Returns Collection for Twitter User Account Information
    def return_twitter_account_collection(self) -> pymongo.collection.Collection:
        self.my_db = self.mongoClient["twitter"]
        self.stats_column = self.my_db["users"]
        return self.stats_column

    # Returns Collection for Twitter User Tweets
    def return_twitter_user_tweet_collection(self) -> pymongo.collection.Collection:
        self.my_db = self.mongoClient["twitter"]
        self.stats_column = self.my_db["tweets"]
        return self.stats_column

    # Returns Collection for Twitter OptIn Users
    def return_opted_in_user_collection(self) -> pymongo.collection.Collection:
        self.my_db = self.mongoClient["twitter"]
        self.stats_column = self.my_db["optedIn"]
        return self.stats_column

    def close_connection(self) -> None:
        self.my_db.close()
