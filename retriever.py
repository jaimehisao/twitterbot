from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys
import uuid

import pprint

#Homemade Classes import
from config import create_api
import mongoer

#API Object from our keys.
api = create_api()

#Retrieve User's information to add to the database
def retrieveBasicInfo() -> None:
    mongo = mongoer.Mongo()
    optedInDatabase = mongo.returnOptedInUsersCollection()
    for user in optedInDatabase.find({}):
        userData = api.get_user(user['screenName'])
    del mongo

def retrieveUsersTweets() -> None:
    #Open Connection to MongoDB and sets the collections to be used
    mongo = mongoer.Mongo()
    userTweets = mongo.returnTwitterUserTweetsCollection()
    optedInDatabase = mongo.returnOptedInUsersCollection()

    #optedInDatabase.insert_one({'_id' : str(uuid.uuid3(name = 'GabsmasterH', namespace = uuid.NAMESPACE_DNS)), 'screenName' : 'GabsmasterH', 'addedAt' : datetime.utcnow()})
    #Retrieves all opted in users in the MongoDB Database and iterates over every single one.
    for user in optedInDatabase.find({}):
        #Add Try and Catch for user not found tweepy.error.TweepError: [{'code': 50, 'message': 'User not found.'}]
        item = api.get_user(user['screenName'])
        print('Querying Tweets from...'+ user['screenName'])
        #For every Tweet from the user in the OptedIn database
        for status in Cursor(api.user_timeline, id=user['screenName']).items():
            #uuidEx = str(uuid.uuid3(name = str(status.text.lower()), namespace = uuid.NAMESPACE_DNS))
            #print(status)
            nameOp = item.name
            screen = item.screen_name
            timestamp = status.created_at
            userMentions = []
            hashtags = []
            statuses = item.statuses_count
            statusText = status.text
            tweetLinkedUrl = None

            ''' 
            ***LOL this totally doesn't work***


            replyStatusId = ""
            replyUserId = ""
            replyUser = ""
            #Fields in case the Tweet is a reply to another tweet
            if (status.in_reply_to_status_id_str is not ""):
                replyStatusId = status.in_reply_to_status_id_str
            
            if (status.in_reply_to_user_id_str is not ""):
                replyUserId = status.in_reply_to_user_id_str

            if (status.in_reply_to_screen_name is not ""):
                replyUser = status.in_reply_to_screen_name
            '''

            replyStatusId = status.in_reply_to_status_id_str
            replyUserId = status.in_reply_to_user_id_str
            replyUser = status.in_reply_to_screen_name

            #Checks if there are users mentioned or hashtags used and adds them to array
            if hasattr(status, "entities"):
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
                                    userMentions.append(name)
                if "urls" in entities:
                    for url in entities["urls"]:
                        if url is not None:
                            if "url" in url:
                                tweetLinkedUrl = url['url']

            #Checks if the Tweet is a Retweet based in the first two char of the string.
            if(statusText[0] == 'R' and statusText[1] == 'T'):
                isRetweet = True
            else:
                isRetweet = False
            
            #Checks if the Tweet isn't already inserted in the DB using the UUID
            if not userTweets.find_one({"_id" : status.id_str}):
                tmpTweet = {'_id' : status.id_str, 'userID' : item.id_str,'name' : nameOp, 'screenName' : screen, 'text' : statusText,
                        'timestamp' : timestamp, 'userMentions' : userMentions, 'hashtags' : hashtags,
                        'replyUser' : replyUser, 'replyUserId' : replyUserId, 'replyStatusId' : replyStatusId,
                        'isRetweet' : isRetweet, 'linkedURL' : tweetLinkedUrl, 'statusesCount' : statuses}
                userTweets.insert_one(tmpTweet)
                print("Inserting Tweet from " + item.name + " with ID " + status.id_str)
            else:
                print("Not Inserting Tweet from " + item.name)
                print("Moving On To Next User... ")
                break

    #Deletes the Mongo object, which closes the connection to the database.
    del mongo

retrieveUsersTweets()