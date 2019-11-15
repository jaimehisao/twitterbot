from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys

#Homemade Classes import
from config import create_api
import mongoer

#API Object from our keys.
api = create_api()

#Account lists to query from the Twitter API
accountsToQuery = ['anaortegon3']

#Queries the accounts of every screen name in the array above
#Returns basic information about the user's account
if len(accountsToQuery) > 0:
    for target in accountsToQuery:
        print("Getting data for " + target)
        item = api.get_user(target)
        print("name: " + item.name)
        print("screen_name: " + item.screen_name)
        print("description: " + item.description)
        print("statuses_count: " + str(item.statuses_count))
        print("friends_count: " + str(item.friends_count))
        print("followers_count: " + str(item.followers_count))

        #Tweet Query in a per user basis
        hashtags = []
        mentions = []
        tweet_count = 0
        #Gets the current time and sets a 30 day back timer.
        end_date = datetime.utcnow() - timedelta(days=30)
        #Returns up to 3200 tweets from the queried user.
        for status in Cursor(api.user_timeline, id=target).items():
            tweet_count += 1
            if hasattr(status, "entities"):
                print(status.text)
                entities = status.entities
                if "hashtags" in entities:
                    for ent in entities["hashtags"]:
                        if ent is not None:
                            if "text" in ent:
                                hashtag = ent["text"]
                                if hashtag is not None:
                                    hashtags.append(hashtag)
                if "user_mentions" in entities:
                    for ent in entities["user_mentions"]:
                        if ent is not None:
                            if "screen_name" in ent:
                                name = ent["screen_name"]
                                if name is not None:
                                    mentions.append(name)
            if status.created_at < end_date:
                break
        
        print
        print("Most mentioned Twitter users:")
        for item, count in Counter(mentions).most_common(10):
            print(item + "\t" + str(count))

        print
        print("Most used hashtags:")
        for item, count in Counter(hashtags).most_common(10):
            print(item + "\t" + str(count))

        print
        print ("All done. Processed " + str(tweet_count) + " tweets.")
        print