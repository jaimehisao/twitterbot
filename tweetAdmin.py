'''
tweetAdmin.py -- Program that allows full CLI Access to the Tweet backend and administration.
By: Jaime Hisao Yesaki A01720044
Version: 0.1
Created on: 7/02/2020
'''

#System Classes
import time
import uuid
import sys
import json

#sys.path.append('/Users/hisao/Documents/Projects/TwitterBot')
#Homemade Classes
from config import create_api
from accounts import addNew
from retriever import retrieveUsersTweetsCLI
from localQuerys import queryByScreenName

#Pip Classes
from pyfiglet import Figlet
from PyInquirer import style_from_dict, Token, prompt, Separator, print_json
from pprint import pprint

#Sentry Error Monitoring
import sentry_sdk
sentry_sdk.init("https://4f9f088dd80c46428a99e34b8ab95b20@sentry.io/3957265")

admin = False

#Calls the retriever.py file and pulls new tweets.
def queryFromTwitter():
    retrieveUsersTweetsCLI()

def systemStatus():
    pass

#Adds user by Twitter Handle
def addUserToQuery():
    requestUserInfo = [
        {
            'type' : 'input',
            'name' : 'userToAdd',
            'message' : '@handle of the user to add - type back to go back'
        }
    ]
    
    ans = prompt(requestUserInfo)
    #print(ans['userToAdd'])
    if (ans['userToAdd'] == 'back'):
        mainMenu()
    else:
        addNew(ans['userToAdd'])

def searchByUsername():
    #Using the username, we fetch the user ID and query the tweets.
    pass


def settingsMenu():
    settingsM = None
    #If the user is admin, the following options are enabled.
    if(admin):
        settingsM = [
            {
            'type' : 'list',
            'name' : 'SettingsMenu',
            'message' : 'What do you want to do?',
            'choices' : [
                'Change automatic Tweet query time',
                'Add Users',
                'Remove Users',
                'List Users',
                'Modify User Privilieges',
                'Back to Main Menu'
            ]
            
            
            }
        ]

    #If the user is not an admin, the following options are enabled.
    else: 
        settingsM = [
            {
            'type' : 'list',
            'name' : 'SettingsMenu',
            'message' : 'What do you want to do?',
            'choices' : [
                'Change automatic Tweet query time',
                Separator(),
                {
                    'name': 'Add Users',
                    'disabled': 'Not enought priviliges'
                },
                {
                    'name': 'Remove Users',
                    'disabled': 'Not enought priviliges'
                },
                {
                    'name': 'List Users',
                    'disabled': 'Not enought priviliges'
                },
                {
                    'name': 'Modify User Privilieges',
                    'disabled': 'Not enought priviliges'
                },
                'Back to Main Menu'
                ]
            
            }
        ]


    ans = prompt(settingsM)
    pprint(ans)

#Menu that responds to the local 
def queryTweetsLocallyMenu():
    localQuery = [
        {
            'type' : 'list',
            'name' : 'QueryMenu',
            'message' : 'What do you want to do?',
            'choices' : [
                'Query by Username',
                'Query by ScreenName',
                'Query by Timeframe',
                'Query by Hashtag'
            ]
        }
    ]

    ans = prompt(localQuery)
    if(ans['QueryMenu'] == 'Query by Username'):
        queryLocallyByUsername()
    else:
        pass


'''
Query Tweets Locally Section
'''

def queryLocallyByUsername():
    options = [
        {
            'type' : 'input',
            'name' : 'theUser',
            'message' : 'Username of the user you want to query locally'
        }
    ]
    screenName = prompt(options)
    queryByScreenName(screenName['theUser'])

def queryLocallyByScreenName():
    pass

def queryLocallyByTimeframe():
    pass

def queryLocallyByHashtag():
    pass


def mainMenu():
    #Intro Text - Displayed when at Main Menu
    f = Figlet(font='slant')
    print(f.renderText('Tweet Admin'))

    #Login to the system, only authorized users can access the DB, query and interact with Tweets.
        #TODO Prompt for username and password, then verify with the DB.
    global admin 
    admin = True

    #Display the main menu
    mainMenu = [
        {
            'type': 'list',
            'name': 'MainMenu',
            'message': 'What do you want to do?',
            'choices': [
                'Manually query new Tweets',
                'Add new users to query',
                'Query Tweets locally',
                'Stats',
                'System Status',
                'Settings',
                'Log Out',
                #Separator(), - ------ line that separates text
                {
                    'name': 'Switch User',
                    'disabled': 'Unavailable at this time'
                }
            ]
        },
    ]

    #Prompt options and then handle the response.
    answers = prompt(mainMenu)
    if(answers['MainMenu'] == 'Manually query new Tweets'):
        #Queries Tweets from the CLOUD Magic.
        queryFromTwitter()
    elif (answers['MainMenu'] == 'Query Tweets locally'):
        #Opens the local tweet query menu
       queryTweetsLocallyMenu()
    elif (answers['MainMenu'] == 'Settings'):
        #Opens the settings menu.
        settingsMenu()
    elif (answers['MainMenu'] == 'Add new users to query'):
        addUserToQuery()
    elif (answers['MainMenu'] == 'Log Out'):
        #Logs out the current user and exits the program.
        #logout()
        exit()
        
#Loop that keeps our menu running always
while True:
    mainMenu()


