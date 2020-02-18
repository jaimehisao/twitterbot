from config import create_api
import pymongo
import tweepy
import mongoer
from datetime import datetime, date, time, timedelta

'''
Methods contained in this file
A) checkIfInDatabase(screenName) - Checks if the user is in the database, returns a boolean and prints it out too.
B) printUsers() - Prints out the users that are in the Opted-In Database.
C) listUsers() - Returns a list with the usernames in the database.
D) addNew(usr) - Adds a new user, in a one by one basis, recieves the user as a parameter.
E) userChangedUsername() - check if the users in the DB have changed their screenName 
F) uuidToTwitterId() - checks if the users in the database have a UUID or a Twitter ID, and changes all accounts that don't to a Twitter Type ID.
'''

#Defunct method that changes the UUID to a Twitter type ID. Used in the past but not at often.
def uuidToTwitterId():
    api = create_api()
    mongo = mongoer.Mongo()
    users = mongo.returnOptedInUsersCollection()
    for user in users.find({}):
        uTemp = api.get_user(user['screenName'])
        users.delete_one({'_id' : user['_id']})
        user['_id'] = uTemp.id_str
        users.insert_one(user)
    del mongo
    print('User records are up to date!')

#This code runs to see if a user changed its username (@user) in Twitter, and update the DB accordingly.
def userChangedUsername() -> None:
    #To run this, users have to have their Twitter ID, so we run that first.
    uuidToTwitterId()
    api = create_api()
    mongo = mongoer.Mongo()
    optedUsers = mongo.returnOptedInUsersCollection()
    for user in optedUsers.find({}):
        try:
            userQuery = api.get_user(user['_id'])
        except:
            print("Error while processing...")
        else:
            if(str(user['screenName']) != str(userQuery.screen_name)):
                print('Screen Name changed. Had:  ' + user['screenName'] + ' now '  + userQuery.screen_name )
                optedUsers.delete_one({'_id' : user['_id']})
                user['screenName'] = userQuery.screen_name
                optedUsers.insert_one(user)

    print('User records are up to date!')
    
#Checks if the user is in the database, returns a boolean and prints it out too.
def checkIfInDatabase(screenName):
    mongo = mongoer.Mongo()
    optedUsers = mongo.returnOptedInUsersCollection()
    if optedUsers.find({'_id':screenName}):
        print(screenName + ' is in the database!')
        return True
    else:
        print(screenName + ' is not in the database!')
        return False

#Prints out the users that are in the Opted-In Database.
def printUsers() -> None:
    mongo = mongoer.Mongo()
    optedUsers = mongo.returnOptedInUsersCollection()
    for user in optedUsers.find({}): 
        print(user['screenName'])
    del mongo

#Returns a list with the usernames in the database.
def listUsers():
    users = []
    users.append()
    mongo = mongoer.Mongo()
    optedUsers = mongo.returnOptedInUsersCollection()
    for user in optedUsers.find({}): 
        users.append(user['screenName'])
    del mongo
    return users

#Adds a new user, in a one by one basis.
def addNew(usr) -> None:
    api = create_api()
    mongo = mongoer.Mongo()
    uTemp = None
    optedInDatabase = mongo.returnOptedInUsersCollection()
    #Checks if the user id exists in Twitter and throws exception if otherwise.
    try:
        uTemp = api.get_user(usr)
    except:
        print('User does not exist.')
    else:
        print('Adding ' + uTemp.id_str + ' with screenName' + uTemp.screen_name)
        #Checks if the user already exists in the DB based on the Twitter ID.
        try:
            user['_id'] = str(uTemp.id) 
            user['screenName'] = uTemp.screen_name 
            user['addedAt'] = datetime.utcnow()
            user['followersCount'] = uTemp.followers_count
            user['friendsCount'] = uTemp.friends_count
            user['createdAt'] = uTemp.created_at
            user['favouritesCount'] = uTemp.favourites_count
            user['statusesCount'] = uTemp.statuses_count
            optedInDatabase.insert_one(user)
        except:
            print('Error when trying to add User...Likely a duplicate!')
    del mongo

userChangedUsername()

'''
#Main, mostly for testing purposes.
mongo = mongoer.Mongo()
userTweets = mongo.returnTwitterUserTweetsCollection()
while True:
    inp = input()
    addNew(inp)
'''

