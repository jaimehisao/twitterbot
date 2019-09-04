'''
streaming.py by Jaime Hisao Yesaki 
Program that connects to the Twitter API and streams tweets instead of querying them in timely intervals.
Created September 3, 2019
Version 0.1
'''
import sys
from config import create_api
from tweepy import Stream
from tweepy import API
from tweepy.streaming import StreamListener

api = create_api()



