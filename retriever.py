# Python Classes
import pprint
import random
import uuid

# Imported Classes
from tweepy import Cursor
import psycopg2
import psycopg2.extras

# Homemade Classes import
import config


# API Object from our keys. -> This creates a connection when the app is launched but we should change this to only
# when the method is being used, besides surrounding it with a try ant catch statement.
api = config.create_api()
psycopg2.extras.register_uuid()


def add_user_if_non_existent(user, cursor, conn) -> None:
    """
    Adds user to the PostgreSQL database when non existent. The method assumes that the user has already been verified
    as non existent and may throw an exception if otherwise.
    :param user: Twitter user object. Straight from the API, no pre-processing.
    :param cursor: Cursor from Psycopg2
    :param conn: Connection from Psycopg2
    """
    cursor.execute('INSERT INTO users (user_id, name, created_at, screen_name, description, url, location, '
                   'verified, tweet_count, follower_count, friends_count) VALUES (%s, %s, %s, %s, %s, %s, %s ,%s, '
                   '%s, %s, %s)',
                   (user.id_str,
                    user.name,
                    user.created_at,
                    user.screen_name,
                    user.description,
                    user.url,
                    user.location,
                    str(int(user.verified)),
                    user.statuses_count,
                    user.followers_count,
                    user.friends_count))
    conn.commit()


# Method that adds tweets to the database and can be called recursively to add tweets that are RT's or mentions.
def tweet_add(status, cursor, conn) -> bool:
    """
    Adds tweet object to the PostgreSQL database. Also adds any existing associations to the Tweet. Eg. the retweeted
    tweet, replied tweet, quoted tweet and all of the users involved in those interactions.
    :param status: Tweepy Status JSON
    :param cursor: Psycopg2 Cursor object
    :param conn: Psycopg2 Connection Object
    :return: boolean value that specifies if the tweet already exists in the DB or not.
    """
    # print('adding tweet...')
    # pprint.pprint(status.user.id)
    tweet_id = status.id_str
    text = status.text
    user = status.user.id
    # print(status.user.screen_name)
    created_at = status.created_at
    language = status.lang
    is_retweet = False
    # retweeted_tweet_id = status.retweeted_status_id_str
    retweeted_tweet_id = None
    is_quote = False
    quote_tweet_id = None
    quote_user_id = None
    reply_to_tweet = status.in_reply_to_status_id_str
    reply_to_user = status.in_reply_to_user_id_str
    hashtags_to_tag = []
    user_mentions_to_tag = []
    tweet_url = None
    tweeted_from = status.source_url

    # Make sure user exists in the DB
    if reply_to_user is not None:
        cursor.execute('SELECT user_id FROM users WHERE user_id = %s', (str(reply_to_user),))
        if len(cursor.fetchall()) == 0:
            print('INFO -> User is not in DB, fetching info from Twitter...' + str(reply_to_user, ))
            try:
                user_fetch = api.get_user(str(reply_to_user, ))
                add_user_if_non_existent(user_fetch, cursor, conn)
            except Exception:
                print('ERROR -> User was not found on Twitter...using same ID but default values...')
                cursor.execute('INSERT INTO users(user_id, "name", created_at) VALUES (%s,%s,%s)', (reply_to_user,
                                                                                                    "User not found",
                                                                                                    '2020-01-01'))
                conn.commit()

    # Make sure user exists in the DB
    cursor.execute('SELECT user_id FROM users WHERE user_id = %s', (str(user),))
    if len(cursor.fetchall()) == 0:
        print('INFO -> User is not in DB, fetching info from Twitter...' + str(user, ))
        try:
            user_fetch = api.get_user(str(user, ))
            add_user_if_non_existent(user_fetch, cursor, conn)
        except Exception:
            print('ERROR -> User was not found on Twitter...using same ID but default values...')
            cursor.execute('INSERT INTO users(user_id, "name", created_at) VALUES (%s,%s,%s)', (user,
                                                                                                "User not found",
                                                                                                '2020-01-01'))
            conn.commit()

    if int(status.retweeted):
        is_retweet = str(int(status.retweeted))
        retweeted_tweet_id = status.retweeted_status_id_str

    if int(status.is_quote_status):
        is_quote = status.is_quote_status
        try:
            quote_tweet_id = status.quoted_status_id_str
        except AttributeError:
            print("Error -> Attribute Tweet ID is not on Status Object")
            quote_tweet_id = random.randint(1, 100000)

        try:
            quote_user_id = status.in_reply_to_user_id_str
        except AttributeError:
            print("Error -> Attribute User ID is not on Status Object")
            quote_user_id = 1

    # Handle hashtags & mentions
    # Checks if there are users mentioned or hashtags used and adds them to array
    if hasattr(status, "entities"):
        entities = status.entities
        if "hashtags" in entities:
            for ent in entities["hashtags"]:
                # print('CONTAINS HASHTAGS')
                if ent is not None:
                    if "text" in ent:
                        hashtag = ent["text"]
                        if hashtag is not None:
                            hashtags_to_tag.append(hashtag)
        if "user_mentions" in entities:
            for ent in entities["user_mentions"]:
                if ent is not None:
                    if "id" in ent:
                        name = ent["id"]
                        if name is not None:
                            user_mentions_to_tag.append(name)
        if "urls" in entities:
            for url in entities["urls"]:
                if url is not None:
                    if "url" in url:
                        tweet_url = url['url']

    if hasattr(status, "retweeted_status"):
        print('INFO -> Is Retweet')
        retweeted_status_attr = status.retweeted_status
        retweeted_tweet_id = retweeted_status_attr.id
        is_retweet = True

        cursor.execute('SELECT * FROM tweet WHERE tweet_id = %s', (retweeted_status_attr.id,))
        if len(cursor.fetchall()) == 0:
            print('INFO -> Inserting RT that was not inserted.')
            try:
                to_send = api.get_status(retweeted_tweet_id)
                tweet_add(to_send, cursor, conn)
            except Exception as ex:
                print('ERROR -> Tweet not found, probably deleted...adding placeholder... ' + str(ex))
                cursor.execute('INSERT INTO tweet(tweet_id, text, "user", is_retweet) VALUES (%s,%s,%s, %s)',
                               (retweeted_tweet_id, "Tweet deleted...", 1, False))
                conn.commit()

    # If Tweet is not on the DB
    cursor.execute('SELECT tweet_id FROM tweet WHERE tweet_id = %s', (tweet_id,))
    if len(cursor.fetchall()) == 0:
        # if tweet is a retweeeted tweet
        if int(status.retweeted):
            print('INFO -> RT')
            # if retweeted tweet is not on the DB
            cursor.execute('SELECT tweet_id FROM tweet WHERE tweet_id = %s', retweeted_tweet_id)
            if len(cursor.fetchall()) == 0:  # Tweet is not on the DB, add it
                to_send = api.get_status(retweeted_tweet_id)
                for send in to_send:
                    tweet_add(send, cursor, conn)
        if is_quote:
            print('INFO -> Quoted Tweet')
            cursor.execute('SELECT * FROM tweet WHERE tweet_id = %s', (quote_tweet_id,))
            if len(cursor.fetchall()) == 0:  # if the quoted tweet is not on the database, add it
                print('INFO -> Quoted tweet is non on the DB...adding ' + str(quote_tweet_id))
                try:
                    if quote_tweet_id is not None:
                        to_send = api.get_status(quote_tweet_id)
                        tweet_add(to_send, cursor, conn)
                except Exception as e:
                    print(
                        'ERROR -> Quoted tweet not found, probably deleted...adding placeholder... EXCEPTION: ' + str(
                            e))
                    # print(quote_user_id)
                    cursor.execute('INSERT INTO tweet(tweet_id, text, "user", is_retweet) VALUES (%s,%s,%s,%s)',
                                   (quote_tweet_id,
                                    "Tweet deleted...",
                                    1, False))
                    conn.commit()
                # pprint.pprint(to_send)
            else:
                # if it is already added we add the new tweet only.
                pass
        if reply_to_tweet is not None:
            print('INFO -> Reply Tweet')
            cursor.execute('SELECT * FROM tweet WHERE tweet_id = %s', (reply_to_tweet,))
            if len(cursor.fetchall()) == 0:
                print('️WARN -> Reply Tweet not on DB...fetching... ' + reply_to_tweet)
                try:
                    to_send = api.get_status(reply_to_tweet)
                    tweet_add(to_send, cursor, conn)
                except Exception as e:
                    print(
                        'ERROR -> Reply tweet is unavailable! ... adding with default values + EXCEPTION: ' + str(e))
                    if reply_to_user is None and reply_to_tweet is None:
                        cursor.execute('INSERT INTO tweet (tweet_id, "user", text) VALUES (%s, %s, %s)',
                                       (random.randint(1, 100000), 1, 'N/A'))
                    else:
                        cursor.execute('INSERT INTO tweet (tweet_id, "user", text) VALUES (%s, %s, %s)',
                                       (reply_to_tweet, reply_to_user, 'N/A'))
                    conn.commit()
                    # pprint.pprint(to_send)
        if True:
            cursor.execute('INSERT INTO tweet (tweet_id, text, "user", created_at, language, is_retweet, '
                           'reply_to_tweet, reply_to_user, is_quote, media_url, quote_tweet_id, quote_user_id, '
                           'tweeted_from, retweeted_tweet_id) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s, %s, '
                           '%s, %s)',
                           (tweet_id, text, user, created_at, language, is_retweet, reply_to_tweet,
                            reply_to_user, is_quote,
                            tweet_url, quote_tweet_id, quote_user_id, tweeted_from, retweeted_tweet_id))
            conn.commit()
            for ht in hashtags_to_tag:
                # TODO add exception for duplicate hashtag key being added as this breaks the program, this generally happens when a Tweet contains the same hashtag two times. -> Done
                # See if hashtag text has already been added into the database.
                cursor.execute('SELECT hashtag_text FROM hashtag WHERE hashtag_text = %s', (ht,))
                if len(cursor.fetchall()) == 0:  # If its not, create UUID and then add to the database
                    hashtag_uuid = uuid.uuid4()
                    cursor.execute('INSERT INTO hashtag(hashtag_id, hashtag_text) VALUES (%s, %s)',
                                   (hashtag_uuid, ht))
                    cursor.execute('SELECT tweet_id, hashtag_id FROM hashtags WHERE tweet_id = %s AND hashtag_id = %s',
                                   (tweet_id, hashtag_uuid))
                    if len(cursor.fetchall()) == 0:
                        cursor.execute('INSERT INTO hashtags(tweet_id, hashtag_id) VALUES (%s, %s)',
                                       (tweet_id, hashtag_uuid))
                    print('INFO -> Adding new hashtag')
                    conn.commit()
                else:
                    # Just add the relation to the hashtags table
                    cursor.execute('SELECT hashtag_id FROM hashtag WHERE hashtag_text = %s', (ht,))
                    hashtag_uuid_imported = cursor.fetchone()[0]
                    cursor.execute('SELECT * FROM hashtags WHERE tweet_id = %s AND hashtag_id = %s',
                                   (tweet_id, hashtag_uuid_imported))
                    if len(
                            cursor.fetchall()) == 0:  # Only adds if the hashtag hasn't been added, case for tweets with two equal tweets
                        cursor.execute('INSERT INTO hashtags(tweet_id, hashtag_id) VALUES (%s, %s)',
                                       (tweet_id, hashtag_uuid_imported))
                        conn.commit()

            for mention in user_mentions_to_tag:
                cursor.execute('SELECT user_id FROM users WHERE user_id = %s', (str(mention),))
                if len(cursor.fetchall()) == 0:
                    print('️WARN -> User is not in DB, searching in Twitter...' + str(mention, ))
                    try:
                        user_fetch = api.get_user(str(mention, ))
                        add_user_if_non_existent(user_fetch, cursor, conn)
                        cursor.execute('INSERT INTO mentions(tweet_id, mentions_user) VALUES (%s, %s)',
                                       (tweet_id, mention))
                        conn.commit()
                    except Exception:
                        print('ERROR -> User not found, using placeholder values')
                        cursor.execute('INSERT INTO mentions(tweet_id, mentions_user) VALUES (%s, %s)',
                                       (tweet_id, 1))
                        conn.commit()
                else:
                    cursor.execute('INSERT INTO mentions(tweet_id, mentions_user) VALUES (%s, %s)',
                                   (tweet_id, mention))
                    conn.commit()
                # Add place to database
                if status.place is not None:
                    cursor.execute('SELECT * FROM place WHERE tweet_id = %s', (tweet_id,))
                    if len(cursor.fetchall()) == 0:
                        cursor.execute('INSERT INTO place (tweet_id, place, country_code) VALUES(%s, %s, %s)',
                                       (tweet_id, status.place.name, status.place.country_code))
                    conn.commit()
            return True
    else:
        print('INFO -> Tweet already added...skipping')
        return False  # Como el tweet ya esta en la base de datos, no lo tenemos que agregar y nos saltamos de usuario.


# Retrieves the tweets from the Opted In Users and adds them to the database.
def retrieve_user_tweets():
    """
    Retrieves the tweets of all users in the user table from PostgreSQL database that have the pull_all flag as true
    """
    # Open Connection to PostgreSQL
    connection = config.connect_to_db()
    cursor = connection.cursor()

    cursor.execute('SELECT user_id, pull_all, name FROM users')
    for user in cursor.fetchall():
        # pBar = tqdm.tqdm(total=len(cursor.fetchall()) - 1)
        num_users = 0
        if user[0] != 1:
            uT = 0
            num_users += 1
            if user[1]:
                try:
                    # input('do you want to continue')
                    # pBar.set_description("Processing tweets from " + user[2])
                    print('INFO -> Fetching user ' + user[2])
                    for status in Cursor(api.user_timeline, id=user[0]).items():
                        stat = tweet_add(status, cursor, connection)
                        uT += 1
                        if not stat:
                            print('INFO -> CHANGING user that is being queried')
                            break
                    print('Tweets queried for ' + str(user[2]) + ' ' + str(uT))
                except Exception as ex:
                    print('ERROR -> User account does not exist or is private. (when querying) ' + str(ex))
        # pBar.update(1)
    print('Finished querying tweets from ' + str(num_users) + ' users.')
    # pBar.close()
    cursor.close()
    connection.close()
