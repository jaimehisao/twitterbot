'''
likeMyTweets.py by Jaime Hisao Yesaki 
This program likes my own tweets and of other certain users that request it through the bot itself.
Created August 1, 2019
Version 1.1
'''

from config import create_api
import tweepy
import logging
import time
import pprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

#Method will fetch tweets and then iterate over them to like them, though this will quickly exahust
#the API Request Limit for starter users
def likeMyTweets(api, since_id):
    logger.info("Retrieving Tweets and finding myself...")
    for tweet in tweepy.Cursor(api.home_timeline, count = 20).items():
        if(tweet.user.screen_name == 'JHisao'):
                try:
                        api.create_favorite(tweet.id)
                        toSend = 'Tweet with ', tweet.id, "liked!"
                        logger.info(toSend)
                except tweepy.TweepError:
                        logger.info("You've already liked this tweet...")

#Method that creates the API object to connect to Twitter and then proceeds to call the likeMyTweets Function
def likeMTweets():
    api = create_api()
    since_id = 1
    while True:
        likeMyTweets(api, since_id)
