"""
tweetTrain.py by Jaime Hisao Yesaki
This program uses saved tweets to generate tweets.
Created January 9, 2020
Version 0.1
"""
import logging
# from textgenrnn import textgenrnn
from langdetect import detect

# Bot Classes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

currLang = ''


# Receives the language code of the tweet and compares it with the langauge that is being processed.
def check_language_match_for_processing(lang_code_str):
    pass


# Receives the Tweet and then returns the language's ISO code
def detect_language(text):
    return detect(text)


def generate_tweet(lang) -> None:
    # Set the language for generation
    global currLang
    currLang = lang


strng = input("Oh hi there!")
print(detect_language(strng))
