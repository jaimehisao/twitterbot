import mongoer
from config import create_api


def updateOptedInDb() -> None:
    for user in optedInDatabase.find({}):
        pass

def removeTweets() -> None:
    mongo = mongoer.Mongo()
    userTweets = mongo.returnTwitterUserTweetsCollection()
    for tweet in userTweets.find({}):
        if(tweet['screenName'] == 'ferrus243'):
            print('Deleting Tweet w/ID ' + tweet['_id'])
            userTweets.delete_one({'_id' : tweet['_id']})
        else:
            print('Not deleting Tweet')
    del mongo

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

additionalUserFieldsAdder()