# Python Classes
import pprint

# Imported Classes
import psycopg2

# Homemade Classes import

# API Object from our keys. -> This creates a connection when the app is launched but we should change this to only
# when the method is being used, besides surrounding it with a try ant catch statement.


connection = psycopg2.connect(user="twitteruser",
                              password="twitterT343432434@",
                              host="services.hisao.org",
                              port="5432",
                              database="twitter")
pprint.pprint(connection)

cursor = connection.cursor()

cursor.execute('SELECT * FROM public.users')
#pprint.pprint(cursor.fetchall())

for item in cursor.fetchall():
    pprint.pprint(item)
    print(item[0])

cursor.close()
connection.close()
