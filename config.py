'''
config.py by Jaime Hisao Yesaki 
This python module returns the API authentication object from enviroment variables that are set
in the computer, then this object can be shared among other program modules.
Created August 2, 2019
Version 1.0
'''
import tweepy
import logging
import os

logger = logging.getLogger()

def create_api():
    #Gets variables from the enviroment (enviroment variables)
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    #Handles authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    
    #Try and catch for credentials, if not possible returns a generic error and prints trace
    try:
        api.verify_credentials()
    except Exception :
        logger.error("Error creating API", exc_info=True)
        #raise e
        
    #Ends Execution and returns API value
    logger.info("API created")
    return api