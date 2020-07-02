import matplotlib.pyplot as plt
import networkx as nx
import psycopg2

connection = psycopg2.connect(user="twitteruser",
                              password="twitterT343432434@",
                              host="services.hisao.org",
                              port="5432",
                              database="twitter")

cursor = connection.cursor()

cursor.execute('SELECT tweet_id, reply_to_tweet FROM tweet LIMIT 100')

tweets = cursor.fetchall()

g = nx.Graph()

for tweet in tweets:
    print(tweet)
    g.add_node(tweet[0])
    g.add_edge(tweet[0], tweet[1])

print(nx.info(g))
nx.draw(g)
plt.show()
