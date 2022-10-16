import psycopg2
import tweepy
from config import create_api
import logging

def import_followers_to_opted_in_users():
    connection = None
    try:
        connection = psycopg2.connect(user="twitteruser",
                                      password="twitterT343432434@",
                                      host="services.hisao.org",
                                      port="5432",
                                      database="twitter")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

        api = create_api()

        for user in tweepy.Cursor(api.friends, screen_name="jaimehisao").items():
            # pprint.pprint(user)

            print(user.screen_name,
                  user.id_str,
                  user.name,
                  user.created_at,
                  user.screen_name,
                  user.description,
                  user.url,
                  user.location)
            cursor.execute('SELECT * from users WHERE user_id = %s', (user.id_str,))
            if len(cursor.fetchall()) == 0:
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
            #cursor.execute('UPDATE users SET pull_all = true WHERE  user_id = %s', (user.id_str,))
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

import_followers_to_opted_in_users()