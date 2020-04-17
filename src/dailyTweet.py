'''
dailyTweet.py by Jaime Hisao Yesaki 
This program uses my main Twitter account as well as other accounta as templates for new auto-generated tweets.
Created August 5, 2019
Version 0.1
'''
import tweepy
import logging
import re  # Regex
from config import create_api
from textgenrnn import textgenrnn

import mongoer

'''
We could also add a functionality that can, based on a Tweet add more users to base our tweets upon
or have an option to add in a "per tweet" basis, to the training model.



#Program reads file-stored tweets, 
def readFromFile():
    print()

def writeToFile():
    
    print()
'''

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# api = create_api()


texts = []
contextLabels = []


# Removes text from tweets that can impact the model negatively.
def processText(text):
    text = re.sub(r'http\S+', '', text)  # Removes URLs included in the Tweet
    text = re.sub(r'@[a-zA-Z0-9_]+', '', text)  # Remove @ mentions in Tweets
    text = text.strip(" ")  # Remove whitespace characters resulting from previus operations
    text = re.sub(r' +', ' ', text)  # Remove redundant spaces (extra)

    # Handle and remove common HTML entities
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&amp;', '&', text)
    return text


def generateTweet() -> None:
    print("Downloading user Tweets...")
    tweetsAdded = 0
    # all_tweets = tweepy.Cursor(api.user_timeline, screen_name = 'JHisao', count = 200, tweet_mode = 'extended', include_rts = False).pages(16)
    mongo = mongoer.Mongo()
    userTweets = mongo.returnTwitterUserTweetsCollection()
    for tweet in userTweets.find({}):
        if (tweet['screenName'] == 'marin_chavarria'):  # TRY AND CATCH IF ARR IS EMPTY
            if True:
                if (tweet['isRetweet'] is not True):
                    tweetText = processText(tweet['text'])
                    if tweetText is not '':
                        texts.append(tweetText)
                        contextLabels.append('all')
                        tweetsAdded = tweetsAdded + 1
        # logger.log(tweetsAdded)
    print(tweetsAdded)

    del mongo

    # textgen = textgenrnn(name='{}_twitter'.format("_".join(cfg['twitter_users'])))
    textgen = textgenrnn(name="marin2")

    textgen.train_new_model(texts, context_labels=contextLabels, gen_epochs=2, batch_size=128, train_size=1.28,
                            rnn_layers=2, rnn_size=128, rnn_bidirectional=False, max_length=40, dim_embeddings=100,
                            word_level=True)
    return textgen


# Use file with stored Tweets to reduce API strain?
def dailyBasedTweet() -> None:
    print()
    # textgen = generateTweet()
    # textgen = textgenrnn('JHisao_twitter_weights.hdf5')
    txtgn = generateTweet()
    txtgn.generate_samples()


dailyBasedTweet()
