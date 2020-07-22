"""
mentions.py by Jaime Hisao Yesaki
This program checks if the bot was mentioned in Twitter and interacts with the user depending on the query.
Created August 1, 2019
Version 1.1
"""
from src.config import create_api
import tweepy
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def check_mentions(api, keywords, since_id):
    logger.info("Retrieving Tweets and Checking for Mentions...")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id, count=10).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to", tweet.user.name)
            api.update_status(
                status="Hola!", in_reply_to_status_id=tweet.id)
    return new_since_id


def handle_mentions():
    # Implement File Reading and Writing for Tweets, both from me and from others...
    api = create_api()
    since_id = 1
    while True:
        print(since_id)
        since_id = check_mentions(api, ["Hola", "Hello", "Queonda"], since_id)
    logger.info("Replying to Tweet Mention...")


def main():
    api = create_api()
    since_id = 1
    while True:
        print(since_id)
        since_id = check_mentions(api, ["Hola", "Hello", "Queonda"], since_id)
        logger.info("Waiting for next program run...")
        time.sleep(60)


if __name__ == "__main__":
    main()
