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
    for tweet in tweepy.Cursor(api.home_timeline).items():
        if(tweet.user.screen_name == 'JHisao'):
                try:
                        api.create_favorite(tweet.id)
                        print('Tweet with ', tweet.id, "liked!")
                except tweepy.TweepError:
                        print("You've already liked this tweet...")


def likeMTweets():
    api = create_api()
    since_id = 1
    while True:
        print(since_id)
        likeMyTweets(api, since_id)
        logger.info("Waiting for next program run...")
        time.sleep(60)
