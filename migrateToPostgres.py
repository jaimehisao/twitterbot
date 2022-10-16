import pprint

import pymongo
import psycopg2

old = pymongo.MongoClient("mongodb://databases.prod.hisao.org:27017/")

connection = None
try:
    connection = psycopg2.connect(user="twitteruser",
                                  password="twitterT343432434@",
                                  host="databases.prod.hisao.org",
                                  port="5432",
                                  database="twitter")

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

    oldDB = old["twitter"]
    oldColumn = oldDB["tweets"]
    oldCursor = oldColumn.find({})

    one = oldColumn.find_one({})

    pprint.pprint(one)

    for tweet in oldCursor:
        pass






except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    # closing database connection.
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

oldDB = old["twitter"]
oldColumn = oldDB["tweets"]

old.close()
