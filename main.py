'''
main.py by Jaime Hisao Yesaki 
This program uses the other members of the project to execute actions at given times of the day to
avoid API bans and rate limiting.
Created August 1, 2019
Version 1.3
'''
import schedule #To run code at specific intervals
import time #To handle and calculate time
from followBack import follow 
from followBack import unfollow
from likeMyTweets import likeMTweets
from mentions import handleMentions
#from dailyTweet import dailyBasedTweet

#Scheduling for tasks that the bot has tu run
#schedule.every().day.at("22:30").do(follow) #Follows Back users that follow the bot
#schedule.every().day.at("01:35").do(unfollow) #Unfollows users that follow the bot
schedule.every().hour.at(":25").do(likeMTweets) #Likes my other (main) account's tweets
#schedule.every().hour.at(":00").do(handleMentions) #Handles Tweet Mentions at each hour
#schedule.every().hour.at(":45").do(handleMentions) #Handles Tweet Mentions at each 45 minute of hour
#schedule.every().day.at("09:00").do(dailyBasedTweet) #Handles Every Day Tweet

#This will run always, checking the scheduler to see if a piece of code has to run at the specified hour and minute, otherwise, go to sleep
while True:
    schedule.run_pending()
    time.sleep(1)
