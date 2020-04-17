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

    def __del__(self):
        self.mongoClient.close()

    # Returns Collection for listening stats
    def return_listening_stats_collection(self) -> pymongo.collection.Collection:
        self.mydb = self.mongoClient["music"]
        self.statsCol = self.mydb["listeningStats"]
        return self.statsCol

    # Returns Collection for Twitter User Account Information
    def return_twitter_account_collection(self) -> pymongo.collection.Collection:
        self.mydb = self.mongoClient["twitter"]
        self.statsCol = self.mydb["users"]
        return self.statsCol

    # Returns Collection for Twitter User Tweets
    def return_twitter_user_tweet_collection(self) -> pymongo.collection.Collection:
        self.mydb = self.mongoClient["twitter"]
        self.statsCol = self.mydb["tweets"]
        return self.statsCol

    # Returns Collection for Twitter OptIn Users
    def return_opted_in_user_collection(self) -> pymongo.collection.Collection:
        self.mydb = self.mongoClient["twitter"]
        self.statsCol = self.mydb["optedIn"]
        return self.statsCol

    def close_connection(self) -> None:
        self.mydb.close()
