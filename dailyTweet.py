'''
dailyTweet.py by Jaime Hisao Yesaki 
This program uses my main Twitter account as a template for new auto-generated tweets.
Created August 5, 2019
Version 0.1
'''
import tweepy
import logging
from config import create_api

#Use file with stored Tweets to reduce API strain?
def dailyBasedTweet():
    print()
