import psycopg2
from neo4j import GraphDatabase

# neo4j Stuff

uri = 'neo4j://localhost:7687'
n4j = GraphDatabase.driver(uri, auth=("neo4j", "password"))

# Postgres Stuff
connection = psycopg2.connect(user="twitteruser",
                              password="twitterT343432434@",
                              host="services.hisao.org",
                              port="5432",
                              database="twitter")
cursor = connection.cursor()


def import_to_neo4j():
    cursor.execute('SELECT * FROM users WHERE pull_all = true LIMIT 100')
    users = cursor.fetchall()

    cursor.execute('SELECT * FROM tweet LIMIT 100')
    tweets = cursor.fetchall()

    for user in users:
        print(user)

    for tweet in tweets:
        print(tweet)
