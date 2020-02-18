import mongoer
from config import create_api


#Temporary fix for duplicate fields - Not in use anymore UserID vs UserId
def removeCapsUserID():
    mongo = mongoer.Mongo()
    userTweets = mongo.returnTwitterUserTweetsCollection()
    userTweets.update({}, {'$unset': {'userID':1}}, multi=True)
    del mongo

#Removes a Tweet by a specific given ID (of the tweet).
def removeTweetsById(id) -> None:
    #Connect the Database
    mongo = mongoer.Mongo()
    userTweets = mongo.returnTwitterUserTweetsCollection()
    #Retrieve the tweets that match the criteria (the ID)
    for tweet in userTweets.find({'_id' : id}):
        pass
    #Delete the tweets
    pass

#Removes Tweets whose author is the User ID given.
def removeTweetsByUser(user) -> None:
    #Connect the Database
    mongo = mongoer.Mongo()
    userTweets = mongo.returnTwitterUserTweetsCollection()
    #Using the screenName, retrieve the user ID 
    id = retrieveUserId(user)
    #Retrieve the tweets that match the criteria (ID, retrieved previusly)
    result = userTweets.delete_many({'_id' : id})
    print(str(result.deleted_count) + ' that matched the criteria were deleted.')
    #Delete the tweets

    pass

'''
retrieveUserId(screenname) - Method that runs and adds the ID of a user to the Tweets stored in the DB.
Parameters: 
    screenName - The screenName of the user that we want to find the ID from.
Returns:
    userId - Returns the ID of the user that matches to the screenName given.
By: Jaime Hisao Yesaki
Date added: 20/01/2020
Version 1.0
'''
#Recieves the user/screename and returns the ID.
def retrieveUserId(screename):
    return 1

'''
addUserIdToTweets() - Method that runs and adds the ID of a user to the Tweets stored in the DB.
Parameters:
    *
Returns:
    *
By: Jaime Hisao Yesaki
Date added: 20/01/2020
Version 1.0
'''
def updateOptedInDb() -> None:
        pass

'''
addUserIdToTweets() - Method that runs and adds the ID of a user to the Tweets stored in the DB.
Parameters:
    N/A
Returns:
    N/A
By: Jaime Hisao Yesaki
Date added: 20/01/2020
Version 1.0
'''
def addUserIdToTweets() -> None:
    mongo = mongoer.Mongo()
    userTweets = mongo.returnTwitterUserTweetsCollection()
    users = mongo.returnOptedInUsersCollection()
    for tweet in userTweets.find({}):
        for user in users.find({'screenName' : tweet['screenName']}):
            changedTweet = tweet
            changedTweet['userId'] = user['_id']
            userTweets.delete_one({'_id' : tweet['_id']})
            userTweets.insert_one(changedTweet)
            print('Attribute added! ' + user['_id'] + ' to ' + user['screenName'] + ' to tweet '+ changedTweet['_id'])
    del mongo

'''
removeTweets() - Method that removes the Tweets from the database, but the parameters are hard coded.
Not for production use 
Parameters:
    *
Returns:
    *
By: Jaime Hisao Yesaki
Date added: 01/01/2020
Version 1.0
'''
def removeTweets() -> None:
    mongo = mongoer.Mongo()
    userTweets = mongo.returnTwitterUserTweetsCollection()
    for tweet in userTweets.find({}):
        if(tweet['screenName'] == 'Galdifab'):
            print('Deleting Tweet w/ID ' + tweet['_id'])
            userTweets.delete_one({'_id' : tweet['_id']})
        else:
            print('Not deleting Tweet')
    del mongo

'''
removeTweets() - Method that adds additional fields to users that do not have them. 
Usually not used, as most are added at first.
Parameters:
    *
Returns:
    *
By: Jaime Hisao Yesaki
Date added: 05/01/2020
Version 1.0
'''
def additionalUserFieldsAdder():
    api = create_api()
    mongo = mongoer.Mongo()
    users = mongo.returnOptedInUsersCollection()
    for user in users.find({}):
        uTemp = api.get_user(user['screenName'])
        users.delete_one({'_id' : user['_id']})
        user['followersCount'] = uTemp.followers_count
        user['friendsCount'] = uTemp.friends_count
        user['createdAt'] = uTemp.created_at
        user['favouritesCount'] = uTemp.favourites_count
        user['statusesCount'] = uTemp.statuses_count
        users.insert_one(user)
    del mongo


#Part where pieces of code are hard coded to run when the file runs
removeCapsUserID()