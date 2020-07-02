"""
followBack.py by Jaime Hisao Yesaki
This program follows and un_follows automatically the users of the bot.
Created August 1, 2019
Version 1.1
"""
from src.auth.config import create_api
import tweepy
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def follow():
    api = create_api()
    # since_id = 1
    for follower in tweepy.Cursor(api.followers, count=20).items():
        follower.follow()
        logger.info("User: " + follower.name + " has been followed!")


def un_follow():
    api = create_api()
    # since_id = 1
    for follower in tweepy.Cursor(api.followers, count=20).items():
        if follower.destroy_friendship:
            api.destroy_friendship(follower.id)
            logger.info("User: {follower} has been unfollowed!")
