'''
tweetAdmin.py -- Program that allows full CLI Access to the Tweet backend and administration.
By: Jaime Hisao Yesaki A01720044
Version: 0.1
Created on: 7/02/2020
'''

# System Classes
import time
import uuid
import sys
import json

# sys.path.append('/Users/hisao/Documents/Projects/TwitterBot')
# Homemade Classes

from src.accounts import add_new_user
from src.retriever import retrieveUsersTweetsCLI

# Pip Classes
from pyfiglet import Figlet
from PyInquirer import style_from_dict, Token, prompt, Separator, print_json
from pprint import pprint

# Sentry Error Monitoring
import sentry_sdk

sentry_sdk.init("https://4f9f088dd80c46428a99e34b8ab95b20@sentry.io/3957265")

admin = False


# Calls the retriever.py file and pulls new tweets.
def query_from_twitter():
    retrieveUsersTweetsCLI()


def system_status():
    pass


def add_user_to_query():
    """Adds user by Twitter Handle."""
    requestUserInfo = [
        {
            'type': 'input',
            'name': 'userToAdd',
            'message': '@handle of the user to add - type back to go back'
        }
    ]

    ans = prompt(requestUserInfo)
    # print(ans['userToAdd'])
    if ans['userToAdd'] == 'back':
        main_menu()
    else:
        add_new_user(ans['userToAdd'])


def search_by_username():
    # Using the username, we fetch the user ID and query the tweets.
    pass


def settings_menu():
    settings_m = None
    # If the user is admin, the following options are enabled.
    if admin:
        settings_m = [
            {
                'type': 'list',
                'name': 'SettingsMenu',
                'message': 'What do you want to do?',
                'choices': [
                    'Change automatic Tweet query time',
                    'Add Users',
                    'Remove Users',
                    'List Users',
                    'Modify User Privilieges',
                    'Back to Main Menu'
                ]

            }
        ]

    # If the user is not an admin, the following options are enabled.
    else:
        settings_m = [
            {
                'type': 'list',
                'name': 'SettingsMenu',
                'message': 'What do you want to do?',
                'choices': [
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

    ans = prompt(settings_m)
    pprint(ans)


# Menu that responds to the local
def query_tweets_locally_menu():
    local_query = [
        {
            'type': 'list',
            'name': 'QueryMenu',
            'message': 'What do you want to do?',
            'choices': [
                'Query by Username',
                'Query by ScreenName',
                'Query by Timeframe',
                'Query by Hashtag'
            ]
        }
    ]

    ans = prompt(local_query)
    if ans['QueryMenu'] == 'Query by Username':
        query_locally_by_username()
    else:
        pass


'''
Query Tweets Locally Section
'''


def query_locally_by_username():
    options = [
        {
            'type': 'input',
            'name': 'theUser',
            'message': 'Username of the user you want to query locally'
        }
    ]
    screen_name = prompt(options)
    query_locally_by_screenname(screen_name['theUser'])


def query_locally_by_screenname():
    pass


def query_locally_by_timeframe():
    pass


def query_locally_by_hashtag():
    pass


def main_menu():
    # Intro Text - Displayed when at Main Menu
    f = Figlet(font='slant')
    print(f.renderText('Tweet Admin'))

    # Login to the system, only authorized users can access the DB, query and interact with Tweets.
    # TODO Prompt for username and password, then verify with the DB.
    global admin
    admin = True

    # Display the main menu
    main_menu_list = [
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
                # Separator(), - ------ line that separates text
                {
                    'name': 'Switch User',
                    'disabled': 'Unavailable at this time'
                }
            ]
        },
    ]

    # Prompt options and then handle the response.
    answers = prompt(main_menu_list)
    if answers['MainMenu'] == 'Manually query new Tweets':
        # Queries Tweets from the CLOUD Magic.
        query_from_twitter()
    elif answers['MainMenu'] == 'Query Tweets locally':
        # Opens the local tweet query menu
        query_tweets_locally_menu()
    elif answers['MainMenu'] == 'Settings':
        # Opens the settings menu.
        settings_menu()
    elif answers['MainMenu'] == 'Add new users to query':
        add_user_to_query()
    elif answers['MainMenu'] == 'Log Out':
        # Logs out the current user and exits the program.
        # logout()
        exit()


# Loop that keeps our menu running always
while True:
    main_menu()
