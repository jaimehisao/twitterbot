"""
config.py by Jaime Hisao Yesaki
This python module returns the API authentication object from enviroment variables that are set
in the computer, then this object can be shared among other program modules.
Created August 2, 2019
Version 1.0
"""
import tweepy
import logging
import os
import dotenv
import psycopg2

dotenv.load_dotenv()  # Loads values from the .env file

logger = logging.getLogger()


def create_api():
    # Get env variables
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    # Handle authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Try and catch for credentials, if not possible returns a generic error and prints trace
    try:
        api.verify_credentials()
    except Exception:
        logger.error("Error creating API", exc_info=True)
        # raise e

    # Ends Execution and returns API value
    logger.info("API created")
    return api


def connect_to_db():
    connection = psycopg2.connect(user="apps",
                                  password="apps_for_postgres_prod",
                                  host="databases.prod.hisao.org",
                                  port="5432",
                                  database="twitter")
    return connection

