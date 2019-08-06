### TwitterBot

## Project Objective
Create a simple bot that runs at specific times during the day to do simple tasks, such as replies, likes, and follows to its 
followers.

The bot runs the tasks at specific times during a day to prevent errors and rate limiting from Twitter's API.


## How does this project work?
Using various open source libraries this project can achieve its given objectives. The program connects to the Twitter API at 
set times during the day to download tweets and interact with users. 

The Project uses libraries like Tweepy to serve as a Twitter API Wrapper and textgenrnn to generate random tweets.

### Project ToDo's 

- Sync Follower & Tweet list locally to reduce the number of queries to Twitter's API
- Make the robot work with Twitter's Stream API to get and interact with Tweets in real time
- Connect the bot to other projects of mine
