"""
tweetOperations.py by Jaime Hisao Yesaki
This program contains operations done on or with tweets.
Created July 24, 2020
Version 1.1
"""
import config
import tweepy
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def follow():
    api = create_api()
    # since_id = 1
    for follower in tweepy.Cursor(api.followers, count=20).items():
        follower.follow()
        logger.info("User: " + follower.name + " has been followed!")


def un_follow():
    api = create_api()
    # since_id = 1
    for follower in tweepy.Cursor(api.followers, count=20).items():
        if follower.destroy_friendship:
            api.destroy_friendship(follower.id)
            logger.info("User: {follower} has been unfollowed!")


def process_text(text) -> str:
    """Removes text from tweets that can impact the model negatively."""
    text = re.sub(r"http\S+", "", text)  # Removes URLs included in the Tweet
    text = re.sub(r"@[a-zA-Z0-9_]+", "", text)  # Remove @ mentions in Tweets
    text = text.strip(
        " "
    )  # Remove whitespace characters resulting from previus operations
    text = re.sub(r" +", " ", text)  # Remove redundant spaces (extra)

    # Handle and remove common HTML entities
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&amp;", "&", text)
    return text


def query_by_screenname(screen_name):
    connection = config.connect_to_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tweets")

    cursor.fetchall()
    print(
        "The user "
        + str(screen_name)
        + " has "
        + len(cursor)
        + " tweets in the database."
    )

    connection.close()


# Removes a Tweet by a specific given ID (of the tweet).
def remove_tweets_by_id(id) -> None:
    # Connect the Database
    mongo = mongoer.Mongo()
    user_tweets = mongo.returnTwitterUserTweetsCollection()
    # Retrieve the tweets that match the criteria (the ID)
    for tweet in user_tweets.find({"_id": id}):
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
    result = user_tweets.delete_many({"_id": user_id})
    print(str(result.deleted_count) + " that matched the criteria were deleted.")
    # Delete the tweets

    pass


"""
retrieveUserId(screenname) - Method that runs and adds the ID of a user to the Tweets stored in the DB.
Parameters: 
    screenName - The screenName of the user that we want to find the ID from.
Returns:
    userId - Returns the ID of the user that matches to the screenName given.
By: Jaime Hisao Yesaki
Date added: 20/01/2020
Version 1.0
"""


# Recieves the user/screename and returns the ID.
def retrieve_user_id(screen_name):
    return 1


"""
addUserIdToTweets() - Method that runs and adds the ID of a user to the Tweets stored in the DB.
Parameters:
    *
Returns:
    *
By: Jaime Hisao Yesaki
Date added: 20/01/2020
Version 1.0
"""


def update_opted_in_db() -> None:
    pass


def add_user_id_to_tweets() -> None:
    """
    addUserIdToTweets() - Method that runs and adds the ID of a user to the Tweets stored in the DB.
    Parameters:
        N/A
    Returns:
        N/A
    By: Jaime Hisao Yesaki
    Date added: 20/01/2020
    Version 1.0
    """
    mongo = mongoer.Mongo()
    user_tweets = mongo.returnTwitterUserTweetsCollection()
    users = mongo.returnOptedInUsersCollection()
    for tweet in user_tweets.find({}):
        for user in users.find({"screenName": tweet["screenName"]}):
            changed_tweet = tweet
            changed_tweet["userId"] = user["_id"]
            user_tweets.delete_one({"_id": tweet["_id"]})
            user_tweets.insert_one(changed_tweet)
            print(
                "Attribute added! "
                + user["_id"]
                + " to "
                + user["screenName"]
                + " to tweet "
                + changed_tweet["_id"]
            )
    del mongo


"""
removeTweets() - Method that removes the Tweets from the database, but the parameters are hard coded.
Not for production use 
Parameters:
    *
Returns:
    *
By: Jaime Hisao Yesaki
Date added: 01/01/2020
Version 1.0
"""


def remove_tweets() -> None:
    mongo = mongoer.Mongo()
    user_tweets = mongo.returnTwitterUserTweetsCollection()
    for tweet in user_tweets.find({}):
        if tweet["screenName"] == "Galdifab":
            print("Deleting Tweet w/ID " + tweet["_id"])
            user_tweets.delete_one({"_id": tweet["_id"]})
        else:
            print("Not deleting Tweet")
    del mongo
