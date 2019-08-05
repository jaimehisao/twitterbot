import schedule #To run code at specific intervals
import time #To handle and calculate time
from followBack import follow 
from likeMyTweets import likeMTweets
from mentions import handleMentions

#Scheduling for tasks that the bot has tu run
schedule.every().day.at("12:00").do(follow) #Follows Back users that follow the bot
schedule.every().day.at("18:00").do(likeMTweets) #Likes my other account's tweets
schedule.every().hour.at(":40").do(handleMentions) #Handles Tweet Mentions





while True:
    schedule.run_pending()
    time.sleep(1)