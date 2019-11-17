from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys
import uuid

#Homemade Classes import
from config import create_api
import mongoer

#API Object from our keys.
api = create_api()

#Retrieve User's information to add to the database
def retrieveBasicInfo() -> None:
    pass

def retrieveUsersTweets() -> None:
    #Open Connection to MongoDB and sets the collection to be used
    mongo = mongoer.Mongo()
    userTweets = mongo.returnTwitterUserTweetsCollection()
    optedInDatabase = mongo.returnOptedInUsersCollection()
    #tweetNumber = userTweets.find({}).sort({"tweetNumber":-1}).limit(1)
    #latestTweet = userTweets.find({}).sort({"timestamp":-1}).limit(1)

    #optedInDatabase.insert_one({'_id' : str(uuid.uuid3(name = 'anaortegon3', namespace = uuid.NAMESPACE_DNS)), 'screenName' : 'anaortegon3', 'addedAt' : datetime.utcnow()})
    #Retrieves all opted in users in the MongoDB Database and iterates over every single one.
    for user in optedInDatabase.find({}):
        item = api.get_user(user['screenName'])
        print('Inserting Tweets from...'+ user['screenName'])
        #For every Tweet from the user in the OptedIn database
        for status in Cursor(api.user_timeline, id=user['screenName']).items():
            uuidEx = str(uuid.uuid3(name = str(status.text.lower()), namespace = uuid.NAMESPACE_DNS))
            nameOp = item.name
            screen = item.screen_name
            timestamp = status.created_at
            userMentions = []
            hashtags = []
            statuses = item.statuses_count
            statusText = status.text
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

            #Checks if the Tweet is a Retweet based in the first two char of the string.
            if(statusText[0] == 'R' and statusText[1] == 'T'):
                isRetweet = True
                print("Is RT")
            else:
                isRetweet = False
                print("Isnt RT")

            #Checks if the Tweet isn't already inserted in the DB using the UUID
            if not userTweets.find_one({"_id" : uuidEx}):
                tmpTweet = {'_id' : uuidEx, 'name' : nameOp, 'screenName' : screen, 'text' : statusText,
                        'timestamp' : timestamp, 'userMentions' : userMentions, 'hashtags' : hashtags,
                        'isRetweet' : isRetweet, 'statusesCount' : statuses}
                userTweets.insert_one(tmpTweet)
                print("Inserting Tweet from " + item.name)
            else:
                print("Not Inserting Tweet from " + item.name)
                print("Moving On To Next User... ")
                break

    #Deletes the Mongo object, which closes the connection to the database.
    del mongo

retrieveUsersTweets()