"""
newMain.py by Jaime Hisao Yesaki
This program uses the other members of the project to execute actions at given times of the day to
avoid API bans and rate limiting.
Created November 17, 2019
Version 1.0
"""

import schedule  # To run code at specific intervals
import time  # To handle and calculate time

# from followBack import follow
# from followBack import un_follows
# from likeMyTweets import likeMTweets
# from mentions import handleMentions

# Retrieve the Tweets from every user in the optIn database once a day.

#


# Will run script constantly
while True:
    schedule.run_pending()
    time.sleep(1)
