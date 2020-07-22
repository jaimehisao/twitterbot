"""
accounts.py
Copyright Jaime Hisao, April 2020

This code should not be used for malicious purpose and the creator is not held responsible in any case.
"""
from src.config import create_api
import src.mongoer
from datetime import datetime

'''
Methods contained in this file
A) checkIfInDatabase(screenName) - Checks if the user is in the database, returns a boolean and prints it out too.
B) printUsers() - Prints out the users that are in the Opted-In Database.
C) listUsers() - Returns a list with the usernames in the database.
D) addNew(usr) - Adds a new user, in a one by one basis, recieves the user as a parameter.
E) userChangedUsername() - check if the users in the DB have changed their screenName 
F) uuidToTwitterId() - checks if the users in the database have a UUID or a Twitter ID, and changes all accounts that 
don't to a Twitter Type ID.
'''


def uuid_to_twitter_id():
    # Defunct method that changes the UUID to a Twitter type ID. Used in the past but not at often.
    api = create_api()
    mongo = str.mongoer.Mongo()
    users = mongo.returnOptedInUsersCollection()
    for user in users.find({}):
        u_temp = api.get_user(user['screenName'])
        users.delete_one({'_id': user['_id']})
        user['_id'] = u_temp.id_str
        users.insert_one(user)
    del mongo
    print('User records are up to date!')


def user_changed_username() -> None:
    """This code runs to see if a user changed its username (@user) in Twitter, and update the DB accordingly."""
    uuid_to_twitter_id()  # To run this, users have to have their Twitter ID, so we run that first.
    api = create_api()
    mongo = src.mongoer.Mongo()
    opted_users = mongo.return_opted_in_user_collection()
    for user in opted_users.find({}):
        try:
            user_query = api.get_user(user['_id'])
        except:
            print("Error while processing...")
        else:
            if str(user['screenName']) != str(user_query.screen_name):
                print('Screen Name changed. Had:  ' + user['screenName'] + ' now ' + user_query.screen_name)
                user_query.delete_one({'_id': user['_id']})
                user['screenName'] = user_query.screen_name
                user_query.insert_one(user)

    print('User records are up to date!')


# Checks if the user is in the database, returns a boolean and prints it out too.
def check_if_in_database(screen_name) -> bool:
    mongo = src.mongoer.Mongo()
    opted_users = mongo.return_opted_in_user_collection()
    if opted_users.find({'_id': screen_name}):
        print(screen_name + ' is in the database!')
        return True
    else:
        print(screen_name + ' is not in the database!')
        return False


# Prints out the users that are in the Opted-In Database.
def print_users() -> None:
    mongo = src.mongoer.Mongo()
    optedUsers = mongo.returnOptedInUsersCollection()
    for user in optedUsers.find({}):
        print(user['screenName'])
    del mongo


# Returns a list with the usernames in the database.
def list_users():
    users = []
    mongo = src.mongoer.Mongo()
    opted_users = mongo.returnOptedInUsersCollection()
    for user in opted_users.find({}):
        users.append(user['screenName'])
    del mongo
    return users


# Adds a new user, in a one by one basis.
def add_new_user(usr) -> None:
    api = create_api()
    mongo = src.mongoer.Mongo()
    user_temp = None
    opted_in_database = mongo.return_opted_in_user_collection()

    # Checks if the user id exists in Twitter and throws exception if otherwise.
    try:
        user_temp = api.get_user(usr)
    except:
        print('User does not exist.')
    else:
        print('Adding ' + user_temp.id_str + ' with screenName ' + user_temp.screen_name)
        # Checks if the user already exists in the DB based on the Twitter ID.
        user = {'_id': str(user_temp.id), 'screenName': user_temp.screen_name, 'addedAt': datetime.utcnow(),
                'followersCount': user_temp.followers_count, 'friendsCount': user_temp.friends_count,
                'createdAt': user_temp.created_at, 'favouritesCount': user_temp.favourites_count,
                'statusesCount': user_temp.statuses_count}
        try:
            opted_in_database.insert_one(user)
        except:
            pass
        else:
            print('User ' + user_temp.screen_name + ' added successfully')
        '''
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
        '''
    del mongo


'''
#Main, mostly for testing purposes.
mongo = mongoer.Mongo()
userTweets = mongo.returnTwitterUserTweetsCollection()
while True:
    inp = input()
    addNew(inp)
'''
