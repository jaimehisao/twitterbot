from config import create_api
import tweepy
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def likeMyTweets(api, since_id):
    logger.info("Retrieving Tweets from myself...")
    for tweet in tweepy.Cursor(api.mentions_timeline).items():
        print(tweet.user.name)
        if(tweet.user.name == '@' + api.me().screen_name):
            print('yes')
            print(tweet.text.lower())
            print(tweet.user.name)


def main():
    api = create_api()
    since_id = 1
    while True:
        print(since_id)
        likeMyTweets(api, since_id)
        logger.info("Waiting for next program run...")
        time.sleep(60)

if __name__ == "__main__":
    main()