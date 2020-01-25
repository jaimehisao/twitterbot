'''
tweetTrain.py by Jaime Hisao Yesaki 
This program uses saved tweets to generate tweets.
Created January 9, 2020
Version 0.1
'''
import tweepy
import logging
import re #Regex
#from textgenrnn import textgenrnn
from langdetect import detect

#Bot Classes 
import mongoer
from config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

currLang = ''

#Recieves the language code of the tweet and compares it with the langauge that is being processed.
def checkLanguangeMatchForProcessing(langCodeStr):
    pass

#Recieves the Tweet and then returns the language's ISO code
def detectLanguage(text):
    return detect(text)

def cleanText(text):
    text = re.sub(r'http\S+', '', text)   #Removes URLs included in the Tweet
    text = re.sub(r'@[a-zA-Z0-9_]+', '', text)  #Remove @ mentions in Tweets
    text = text.strip(" ")   #Remove whitespace characters resulting from previus operations
    text = re.sub(r' +', ' ', text)   #Remove redundant spaces (extra)

    #Handle and remove common HTML entities
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&amp;', '&', text)
    return text

def generateTweet(lang) -> None:
    #Set the language for generation
    global currLang
    currLang = lang

strng = input("Oh hi there!")
print(detectLanguage(strng))

