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
'''

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
def addNew(usr)->None:
    api = create_api()
    mongo = mongoer.Mongo()
    uTemp = api.get_user(usr)
    print(uTemp.id_str)
    optedInDatabase = mongo.returnOptedInUsersCollection()
    try:
        optedInDatabase.insert_one({'_id' : str(uTemp.id), 'screenName' : usr, 'addedAt' : datetime.utcnow()})
    except:
        print('Error when trying to add User...May be a duplicate or the user does not exist')
    del mongo






'''
#Main, mostly for testing purposes.
mongo = mongoer.Mongo()
userTweets = mongo.returnTwitterUserTweetsCollection()
while True:
    inp = input()
    addNew(inp)
'''

