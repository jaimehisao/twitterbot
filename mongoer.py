'''
mongoer.py by Jaime Hisao Yesaki 
This program connects to MongoDB and saves the tweets to the database
Created November 14, 2019
Version 0.1
'''

import pymongo

class Mongo:
    def __init__(self):
        self.mongoClient = pymongo.MongoClient("mongodb://10.0.0.4:27017/")

    def __del__(self):
        self.mongoClient.close()

    #Returns Collection for listening stats
    def returnListentingStatsCollection(self) -> pymongo.collection.Collection:
        self.mydb = self.mongoClient["music"]
        self.statsCol = self.mydb["listeningStats"]
        return self.statsCol

    #Returns Collection for Twitter User Account Information
    def returnTwitterAccountCollection(self) -> pymongo.collection.Collection:
        self.mydb = self.mongoClient["twitter"]
        self.statsCol = self.mydb["users"]
        return self.statsCol

    #Returns Collection for Twitter User Tweets
    def returnTwitterUserTweetsCollection(self) -> pymongo.collection.Collection:
        self.mydb = self.mongoClient["twitter"]
        self.statsCol = self.mydb["tweets"]
        return self.statsCol

    #Returns Collection for Twitter OptIn Users
    def returnOptedInUsersCollection(self) -> pymongo.collection.Collection:
        self.mydb = self.mongoClient["twitter"]
        self.statsCol = self.mydb["optedIn"]
        return self.statsCol

    def closeConnection(self) -> None:
        self.mydb.close()