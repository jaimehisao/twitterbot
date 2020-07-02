from tweepy import Cursor

# Homemade Classes import
from src.auth.config import create_api
import src.databases.mongoer

# Progress Bar
from tqdm import tqdm

# API Object from our keys. -> This creates a connection when the app is launched but we should change this to only
# when the method is being used, besides surrounding it with a try ant catch statement.
api = create_api()


# Retrieves Tweets from an individual user, the username is sent as a parameter.
def retrieve_user_tweets_cli() -> None:
    # Open Connection to MongoDB and sets the collections to be used
    mongo = src.databases.mongoer.Mongo()
    user_tweets = mongo.return_twitter_user_tweet_collection()
    opted_in_database = mongo.return_opted_in_user_collection()
    num_tweets = 0
    users_with_errors = []
    # optedInDatabase.insert_one({'_id' : str(uuid.uuid3(name = 'GabsmasterH', namespace = uuid.NAMESPACE_DNS)),
    # 'screenName' : 'GabsmasterH', 'addedAt' : datetime.utcnow()}) Retrieves all opted in users in the MongoDB
    # Database and iterates over every single one.
    retrieved = opted_in_database.find({})
    pBar = tqdm(total=retrieved.count() - 1)
    # pBar = tqdm(retrieved)
    for user in retrieved:
        pBar.set_description("Processing tweets from " + user['screenName'])
        usr_tweet_num = 0
        # Add Try and Catch for user not found tweepy.error.TweepError: [{'code': 50, 'message': 'User not found.'}]
        try:
            item = api.get_user(user['screenName'])  # Retrieve the user using the screenName
            # Maybe this error could be saved is the user ID is used.
        except:
            users_with_errors.append(user['screenName'])  # Append users w/errors
        else:
            # print('Querying Tweets from...'+ user['screenName'])
            # For every Tweet from the user in the OptedIn database
            for status in Cursor(api.user_timeline, id=user['screenName']).items():
                # uuidEx = str(uuid.uuid3(name = str(status.text.lower()), namespace = uuid.NAMESPACE_DNS))
                # print(status)
                name_op = item.name
                screen = item.screen_name
                timestamp = status.created_at
                user_mentions = []
                hashtags = []
                statuses = item.statuses_count
                status_text = status.text
                tweet_linked_url = None

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

                # Checks if there are users mentioned or hashtags used and adds them to array
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
                                        user_mentions.append(name)
                    if "urls" in entities:
                        for url in entities["urls"]:
                            if url is not None:
                                if "url" in url:
                                    tweet_linked_url = url['url']

                # Checks if the Tweet is a Retweet based in the first two char of the string.
                if status_text[0] == 'R' and status_text[1] == 'T':
                    is_retweet = True
                else:
                    is_retweet = False

                # Checks if the Tweet isn't already inserted in the DB using the UUID
                if not user_tweets.find_one({"_id": status.id_str}):
                    tmp_tweet = {'_id': status.id_str, 'userId': item.id_str, 'name': name_op, 'screenName': screen,
                                 'text': status_text, 'timestamp': timestamp, 'userMentions': user_mentions,
                                 'hashtags': hashtags, 'replyUser': replyUser, 'replyUserId': replyUserId,
                                 'replyStatusId': replyStatusId, 'isRetweet': is_retweet, 'linkedURL': tweet_linked_url,
                                 'statusesCount': statuses}
                    user_tweets.insert_one(tmp_tweet)
                    # print("Inserting Tweet from " + item.name + " with ID " + status.id_str)
                    num_tweets += 1
                    usr_tweet_num += 1
                else:
                    break
            # print('Tweets queried from '+ user['screenName']+ ' ' + str(usrTweetNum))
            pBar.update(1)
        # Deletes the Mongo object, which closes the connection to the database.
    print(str(num_tweets) + ' tweets were queried and added to the database!')
    del mongo
    pBar.close()
    if len(users_with_errors) > 0:
        for usersWErrors in users_with_errors:
            print('User ' + usersWErrors + ' generated an error while querying for Tweets...')


# Retrieves Tweets from an individual user, the username is sent as a parameter.
def retrieve_tweets(screen_name) -> None:
    # Open Connection to MongoDB and sets the collections to be used
    mongo = src.databases.mongoer.Mongo()
    user_tweets = mongo.return_twitter_user_tweet_collection()
    user_tweet_num = 0
    # Add Try and Catch for user not found tweepy.error.TweepError: [{'code': 50, 'message': 'User not found.'}]
    try:
        item = api.get_user(screen_name)
    except:
        print(
            'An error ocurred while quering tweets from: ' + screen_name + '...user likely changed screenName or '
                                                                           'account is unavailable...')
    else:
        # For every Tweet of the given screenName
        for status in Cursor(api.user_timeline, id=screen_name).items():
            # uuidEx = str(uuid.uuid3(name = str(status.text.lower()), namespace = uuid.NAMESPACE_DNS))
            # print(status)
            name_op = item.name
            screen = item.screen_name
            timestamp = status.created_at
            user_mentions = []
            hashtags = []
            statuses = item.statuses_count
            status_text = status.text
            tweet_linked_url = None

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

            reply_status_id = status.in_reply_to_status_id_str
            reply_user_id = status.in_reply_to_user_id_str
            reply_user = status.in_reply_to_screen_name

            # Checks if there are users mentioned or hashtags used and adds them to array
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
                                    user_mentions.append(name)
                if "urls" in entities:
                    for url in entities["urls"]:
                        if url is not None:
                            if "url" in url:
                                tweet_linked_url = url['url']

            # Checks if the Tweet is a Retweet based in the first two char of the string.
            if status_text[0] == 'R' and status_text[1] == 'T':
                is_retweet = True
            else:
                is_retweet = False

            # Checks if the Tweet isn't already inserted in the DB using the UUID
            if not user_tweets.find_one({"_id": status.id_str}):
                tmp_tweet = {'_id': status.id_str, 'userID': item.id_str, 'name': name_op, 'screenName': screen,
                             'text': status_text,
                             'timestamp': timestamp, 'userMentions': user_mentions, 'hashtags': hashtags,
                             'replyUser': reply_user, 'replyUserId': reply_user_id, 'replyStatusId': reply_status_id,
                             'isRetweet': is_retweet, 'linkedURL': tweet_linked_url, 'statusesCount': statuses}
                user_tweets.insert_one(tmp_tweet)
                # print("Inserting Tweet from " + item.name + " with ID " + status.id_str)
                user_tweet_num += 1
            else:
                # print("Not Inserting Tweet from " + item.name)
                # print("Moving On To Next User... ")
                break
    # print('Tweets queried from '+ screenName + ' ' + str(usrTweetNum))
    # Deletes the Mongo object, which closes the connection to the database.
    del mongo


# Retrieve User's information to add to the database - Incomplete
def retrieve_basic_info() -> None:
    mongo = src.databases.mongoer.Mongo()
    opted_in_database = mongo.returnOptedInUsersCollection()
    for user in opted_in_database.find({}):
        user_data = api.get_user(user['screenName'])
    del mongo


# Retrieves the tweets from the Opted In Users and adds them to the database.
def retrieve_user_tweets() -> None:
    # Open Connection to MongoDB and sets the collections to be used
    mongo = src.databases.mongoer.Mongo()
    user_tweets = mongo.return_twitter_user_tweet_collection()
    opted_in_database = mongo.return_opted_in_user_collection()
    num_tweets = 0
    # optedInDatabase.insert_one({'_id' : str(uuid.uuid3(name = 'GabsmasterH', namespace = uuid.NAMESPACE_DNS)),
    # 'screenName' : 'GabsmasterH', 'addedAt' : datetime.utcnow()}) Retrieves all opted in users in the MongoDB
    # Database and iterates over every single one.
    for user in opted_in_database.find({}):
        usr_tweet_num = 0
        # Add Try and Catch for user not found tweepy.error.TweepError: [{'code': 50, 'message': 'User not found.'}]
        try:
            item = api.get_user(user['screenName'])
        except:
            print('An error ocurred...User likely changed screenName or account is unavailable...')
            print('This while quering tweets from: ' + user['screenName'] + '...')
        else:
            # print('Querying Tweets from...'+ user['screenName'])
            # For every Tweet from the user in the OptedIn database
            for status in Cursor(api.user_timeline, id=user['screenName']).items():
                # uuidEx = str(uuid.uuid3(name = str(status.text.lower()), namespace = uuid.NAMESPACE_DNS))
                # print(status)
                name_op = item.name
                screen = item.screen_name
                timestamp = status.created_at
                user_mentions = []
                hashtags = []
                statuses = item.statuses_count
                status_text = status.text
                tweet_linked_url = None

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
                reply_user_id = status.in_reply_to_user_id_str
                reply_user = status.in_reply_to_screen_name

                # Checks if there are users mentioned or hashtags used and adds them to array
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
                                        user_mentions.append(name)
                    if "urls" in entities:
                        for url in entities["urls"]:
                            if url is not None:
                                if "url" in url:
                                    tweet_linked_url = url['url']

                # Checks if the Tweet is a Retweet based in the first two char of the string.
                if status_text[0] == 'R' and status_text[1] == 'T':
                    is_retweet = True
                else:
                    is_retweet = False

                # Checks if the Tweet isn't already inserted in the DB using the UUID
                if not user_tweets.find_one({"_id": status.id_str}):
                    tmp_tweet = {'_id': status.id_str, 'userId': item.id_str, 'name': name_op, 'screenName': screen,
                                 'text': status_text,
                                 'timestamp': timestamp, 'userMentions': user_mentions, 'hashtags': hashtags,
                                 'replyUser': reply_user, 'replyUserId': reply_user_id, 'replyStatusId': replyStatusId,
                                 'isRetweet': is_retweet, 'linkedURL': tweet_linked_url, 'statusesCount': statuses}
                    user_tweets.insert_one(tmp_tweet)
                    # print("Inserting Tweet from " + item.name + " with ID " + status.id_str)
                    num_tweets += 1
                    usr_tweet_num += 1
                else:
                    break
            print('Tweets queried from ' + user['screenName'] + ' ' + str(usr_tweet_num))

        # Deletes the Mongo object, which closes the connection to the database.
    print(num_tweets)
    del mongo

