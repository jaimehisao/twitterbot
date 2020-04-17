'''
optIn.py by Jaime Hisao Yesaki 
This program looks for opt in messages in @hisaobot1 and adds the users to the opt in database so their tweets
are now queried, followed and stored, for all the purposes that that involves.
Created November 15, 2019
Version 0.1
'''

import tweepy
import mongoer

#Look for @hisaobot1 tweets in the database and process information with those

#Queries the database and checks the latest tweets from today, then checks if Opt status changed per user
def checkOptIns() -> None:
    #Instantiate the Connection to MongoDB and retrieve the collection to use
    mongo = mongoer.Mongo()
    optedIn = mongo.returnOptedInUsersCollection()

    #Get today's tweets
    optedIn.find_one({})

    del mongo #Deletes Mongo Object to effectively close the connection