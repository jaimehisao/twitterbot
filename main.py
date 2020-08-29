"""
main.py by Jaime Hisao Yesaki
This program uses the other members of the project to execute actions at given times of the day to
avoid API bans and rate limiting.
Created August 1, 2019
Version 1.3
"""
import schedule  # To run code at specific intervals
import time  # To handle and calculate time

import sys

import sentry_sdk

sys.path.append('/usr/code/src')

sentry_sdk.init("https://75642e664d814773b15d11fa487da198@o285082.ingest.sentry.io/5307624")

from likeMyTweets import like_my_tweets

from retriever import retrieve_user_tweets

from link_keywords_to_tweets import get_keywords_for_all_tweets



# from dailyTweet import dailyBasedTweet

# Scheduling for tasks that the bot has tu run
# schedule.every().day.at("22:30").do(follow) #Follows Back users that follow the bot
# schedule.every().day.at("01:35").do(un_follow) #Unfollows users that follow the bot
schedule.every(180).minutes.do(like_my_tweets)
# schedule.every().hour.at(":00").do(handle_mentions) #Handles Tweet Mentions at each hour
# schedule.every().hour.at(":45").do(handle_mentions) #Handles Tweet Mentions at each 45 minute of hour
# schedule.every().day.at("09:00").do(daily_based_tweets) #Handles Every Day Tweet

schedule.every().hour.at(":01").do(retrieve_user_tweets)  # Download new tweets

# This will run always, checking the scheduler to see if a piece of code has to run at the specified hour and minute,
# otherwise, go to sleep
while True:
    # print(sys.path)
    schedule.run_pending()
    time.sleep(1)
