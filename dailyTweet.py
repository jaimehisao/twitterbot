'''
dailyTweet.py by Jaime Hisao Yesaki 
This program uses my main Twitter account as well as others as a template for new auto-generated tweets.
Created August 5, 2019
Version 0.1
'''
import tweepy
import logging
import re #Regex
from config import create_api
from textgenrnn import textgenrnn
from config import create_api

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

api = create_api()

texts = []
contextLabels = []

def processText(text):
    text = re.sub(r'http\S+', '', text)   #Removes URLs included in the Tweet
    text = re.sub(r'@[a-zA-Z0-9_]+', '', text)  #Remove @ mentions in Tweets
    text = text.strip(" ")   #Remove whitespace characters resulting from previus operations
    text = re.sub(r' +', ' ', text)   #Remove redundant spaces (extra)

    #Handle common HTML entities
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&amp;', '&', text)
    return text

def generateTweet():
    print("Downloading user Tweets...")
    all_tweets = tweepy.Cursor(api.user_timeline, screen_name = 'JHisao', count = 200, tweet_mode = 'extended', include_rts = False).pages(16)

    for page in all_tweets:
        for tweet in page:
            tweetText = processText(tweet.full_text)
            if tweetText is not '':
                texts.append(tweetText)
                contextLabels.append('JHisao')
    

    #textgen = textgenrnn(name='{}_twitter'.format("_".join(cfg['twitter_users'])))
    textgen = textgenrnn(name= "JHisao_twitter")

    textgen.train_new_model(texts, context_labels = contextLabels, gen_epochs = 200, batch_size = 128, train_size= 1.28, rnn_layers = 2, rnn_size = 128, rnn_bidirectional = False, max_length = 40, dim_embeddings = 100, word_level = True)
    return textgen


#Use file with stored Tweets to reduce API strain?
def dailyBasedTweet():
    print()
    #textgen = generateTweet()
    textgen = textgenrnn('JHisao_twitter_weights.hdf5')

    textgen.generate_samples()
