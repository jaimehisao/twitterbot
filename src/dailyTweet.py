"""
dailyTweet.py by Jaime Hisao Yesaki
This program uses my main Twitter account as well as other accounta as templates for new auto-generated tweets.
Created August 5, 2019
Version 0.1
"""
import logging
from textgenrnn import textgenrnn
from src.commonUtils import process_text

import src.mongoer

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


def generate_tweet():
    print("Downloading user Tweets...")
    tweets_added = 0
    # all_tweets = tweepy.Cursor(api.user_timeline, screen_name = 'JHisao', count = 200, tweet_mode = 'extended',
    # include_rts = False).pages(16)
    mongo = src.mongoer.Mongo()
    user_tweets = mongo.return_twitter_user_tweet_collection()
    for tweet in user_tweets.find({}):
        if tweet['screenName'] == 'marin_chavarria':  # TRY AND CATCH IF ARR IS EMPTY
            if True:
                if tweet['isRetweet'] is not True:
                    tweet_text = process_text(tweet['text'])
                    if tweet_text is not '':
                        texts.append(tweet_text)
                        contextLabels.append('all')
                        tweets_added = tweets_added + 1
        # logger.log(tweetsAdded)
    print(tweets_added)

    del mongo

    # textgen = textgenrnn(name='{}_twitter'.format("_".join(cfg['twitter_users'])))
    text_gen = textgenrnn(name="marin2")

    text_gen.train_new_model(texts, context_labels=contextLabels, gen_epochs=2, batch_size=128, train_size=1.28,
                            rnn_layers=2, rnn_size=128, rnn_bidirectional=False, max_length=40, dim_embeddings=100,
                            word_level=True)
    return text_gen


# Use file with stored Tweets to reduce API strain?
def daily_based_tweet() -> None:
    print()
    # textgen = generateTweet()
    # textgen = textgenrnn('JHisao_twitter_weights.hdf5')
    txt_gn = generate_tweet()
    txt_gn.generate_samples()


daily_based_tweet()
