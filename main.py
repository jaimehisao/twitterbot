'''
main.py by Jaime Hisao Yesaki 
This program uses the other members of the project to execute actions at given times of the day to
avoid API bans and rate limiting.
Created August 1, 2019
Version 1.1
'''
import schedule #To run code at specific intervals
import time #To handle and calculate time
from followBack import follow 
from followBack import unfollow
from likeMyTweets import likeMTweets
from mentions import handleMentions

#Scheduling for tasks that the bot has tu run
schedule.every().day.at("12:00").do(follow) #Follows Back users that follow the bot
schedule.every().day.at("1:00").do(unfollow) #Unfollows users that follow the bot
schedule.every().day.at("18:00").do(likeMTweets) #Likes my other account's tweets
schedule.every().hour.at(":40").do(handleMentions) #Handles Tweet Mentions

while True:
    schedule.run_pending()
    time.sleep(1)