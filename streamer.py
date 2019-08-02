import tweepy
import os

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

def create_stream():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)

    stream = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener())

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API & Stream", exc_info=True)
        raise e
    logger.info("API & Stream created")
    return myStream