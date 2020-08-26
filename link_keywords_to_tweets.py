# Python Classes
import pprint
import random
import uuid

# Imported Classes
from tweepy import Cursor
import psycopg2
import psycopg2.extras
import tqdm

# Homemade Classes import
import config

import requests
import json

import concurrent.futures
import threading
import time


# API Object from our keys. -> This creates a connection when the app is launched but we should change this to only
# when the method is being used, besides surrounding it with a try ant catch statement.
api = config.create_api()
psycopg2.extras.register_uuid()
thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def get_keywords(tweet):
    connection = config.connect_to_db()
    cursor = connection.cursor()
    # extract the keywords
    data = {'text': tweet[0]}
    response = requests.post('http://keywords.dev.major-tom.googleinterns.app', json=data)
    response = json.loads(response.text)
    print(response)
    if 'tokens' in response:
        for keyword in response["tokens"]:
            cursor.execute('SELECT * FROM keywords WHERE tweet_id = %s and lemma = %s', (tweet[1], keyword["lemma"]))
            if len(cursor.fetchall()) == 0:
                cursor.execute('INSERT INTO keywords(tweet_id, lemma, part_of_speech, word) VALUES (%s, %s, %s, %s)',
                               (tweet[1], keyword["lemma"], keyword["part_of_speech"], keyword["word"]))
                connection.commit()


def get_keywords_for_all_tweets():
    connection = config.connect_to_db()
    cursor = connection.cursor()
    cursor.execute(
        'SELECT text, tweet_id FROM tweet EXCEPT SELECT text, keywords.tweet_id FROM keywords, tweet WHERE tweet.tweet_id = keywords.tweet_id')
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(get_keywords, cursor.fetchall())


def attach_keywords_to_tweets():
    connection = config.connect_to_db()
    cursor = connection.cursor()

    cursor.execute('SELECT text, tweet_id FROM tweet EXCEPT SELECT text, keywords.tweet_id FROM keywords, tweet WHERE tweet.tweet_id = keywords.tweet_id')
    for tweet in cursor.fetchall():
        # extract the keywords
        data = {'text': tweet[0]}
        response = requests.post('http://keywords.dev.major-tom.googleinterns.app', json=data)
        response = json.loads(response.text)
        print(response)
        if 'tokens' in response:
            for keyword in response["tokens"]:
                cursor.execute('SELECT * FROM keywords WHERE tweet_id = %s and lemma = %s', (tweet[1], keyword["lemma"]))
                if len(cursor.fetchall()) == 0:
                    cursor.execute('INSERT INTO keywords(tweet_id, lemma, part_of_speech, word) VALUES (%s, %s, %s, %s)',
                           (tweet[1], keyword["lemma"], keyword["part_of_speech"], keyword["word"]))
                    connection.commit()

    cursor.close()
    connection.close()
