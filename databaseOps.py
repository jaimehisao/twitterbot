from config import create_api
import mongoer


def add_user_id_to_tweets():
    mongo = mongoer.Mongo()
    user_tweets = mongo.returnTwitterUserTweetsCollection()
    opted_in = mongo.returnOptedInUsersCollection()

    # Finds and retrieves all users that have optedIn to have their tweets retrieved.
    for user in opted_in.find({}):
        print('Adding User ID to Tweets from ' + user['screenName'])
        total_tweets = 0
        # For all the users that opted in to have their tweets queried, recieve them.
        for tweet in user_tweets.find({'screenName': user['screenName']}):
            # Work on the tweets, by Adding the User ID field.
            user_tweets.delete_one({'_id': tweet['_id']})
            tweet['userId'] = user['_id']
            user_tweets.insert_one(tweet)
            print('Tweet w/ID ' + tweet['_id'] + 'was added the UID ' + user['_id'])
            total_tweets += 1
        print(total_tweets)


# Temporary fix for duplicate fields - Not in use anymore UserID vs UserId
def remove_caps_user_id():
    mongo = mongoer.Mongo()
    user_tweets = mongo.returnTwitterUserTweetsCollection()
    user_tweets.update({}, {'$unset': {'userID': 1}}, multi=True)
    del mongo


# Removes a Tweet by a specific given ID (of the tweet).
def remove_tweets_by_id(id) -> None:
    # Connect the Database
    mongo = mongoer.Mongo()
    user_tweets = mongo.returnTwitterUserTweetsCollection()
    # Retrieve the tweets that match the criteria (the ID)
    for tweet in user_tweets.find({'_id': id}):
        pass
    # Delete the tweets
    pass


# Removes Tweets whose author is the User ID given.
def remove_tweets_by_user(user) -> None:
    # Connect the Database
    mongo = mongoer.Mongo()
    user_tweets = mongo.returnTwitterUserTweetsCollection()
    # Using the screenName, retrieve the user ID
    user_id = retrieve_user_id(user)
    # Retrieve the tweets that match the criteria (ID, retrieved previusly)
    result = user_tweets.delete_many({'_id': user_id})
    print(str(result.deleted_count) + ' that matched the criteria were deleted.')
    # Delete the tweets

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


# Recieves the user/screename and returns the ID.
def retrieve_user_id(screen_name):
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


def update_opted_in_db() -> None:
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


def add_user_id_to_tweets() -> None:
    mongo = mongoer.Mongo()
    user_tweets = mongo.returnTwitterUserTweetsCollection()
    users = mongo.returnOptedInUsersCollection()
    for tweet in user_tweets.find({}):
        for user in users.find({'screenName': tweet['screenName']}):
            changed_tweet = tweet
            changed_tweet['userId'] = user['_id']
            user_tweets.delete_one({'_id': tweet['_id']})
            user_tweets.insert_one(changed_tweet)
            print('Attribute added! ' + user['_id'] + ' to ' + user['screenName'] + ' to tweet ' + changed_tweet['_id'])
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


def remove_tweets() -> None:
    mongo = mongoer.Mongo()
    user_tweets = mongo.returnTwitterUserTweetsCollection()
    for tweet in user_tweets.find({}):
        if tweet['screenName'] == 'Galdifab':
            print('Deleting Tweet w/ID ' + tweet['_id'])
            user_tweets.delete_one({'_id': tweet['_id']})
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


def additional_user_fields_adder():
    api = create_api()
    mongo = mongoer.Mongo()
    users = mongo.returnOptedInUsersCollection()
    for user in users.find({}):
        uTemp = api.get_user(user['screenName'])
        users.delete_one({'_id': user['_id']})
        user['followersCount'] = uTemp.followers_count
        user['friendsCount'] = uTemp.friends_count
        user['createdAt'] = uTemp.created_at
        user['favouritesCount'] = uTemp.favourites_count
        user['statusesCount'] = uTemp.statuses_count
        users.insert_one(user)
    del mongo


# Part where pieces of code are hard coded to run when the file runs
add_user_id_to_tweets()
