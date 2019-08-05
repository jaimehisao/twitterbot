from config import create_api
import tweepy
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def followBack(api):
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()
        logger.info("User: {follower} has been followed!")


def follow():
    api = create_api()
    since_id = 1
    while True:
        print(since_id)
        followBack(api)
        logger.info("Waiting for next program run...")
        time.sleep(60)
