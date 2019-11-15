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

#Instantiate the Connection to MongoDB
mongo = mongoer.Mongo()

del mongo