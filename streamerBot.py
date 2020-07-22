import tweepy
from config import create_api
from textwrap import TextWrapper


class StreamWatcherListener(tweepy.StreamListener):
    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')

    def on_status(self, status):
        try:
            print(self.status_wrapper.fill(status.text))
            print('\n %s  %s  via %s\n' % (status.author.screen_name, status.created_at, status.source))
        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print('An error has occured! Status code = %s' % status_code)
        return True  # keep stream alive

    def on_timeout(self):
        print('Snoozing Zzzzzz')


def main():
    # From the Config Class import the API with Authentication handled
    api = create_api()
    stream = tweepy.Stream(api, StreamWatcherListener(), timeout=None)

    # Prompt for mode of streaming
    valid_modes = ['sample', 'filter']
    while True:
        mode = input('Mode? [sample/filter] ')
        if mode in valid_modes:
            break
        print('Invalid mode! Try again.')

    if mode == 'sample':
        stream.sample()

    elif mode == 'filter':
        follow_list = input('Users to follow (comma separated): ').strip()
        track_list = input('Keywords to track (comma seperated): ').strip()
        if follow_list:
            follow_list = [u for u in follow_list.split(',')]
            user_id_list = []
            username_list = []

            for user in follow_list:
                if user.isdigit():
                    user_id_list.append(user)
                else:
                    username_list.append(user)

            for username in username_list:
                user = api.get_user(username)
                user_id_list.append(user.id)

            follow_list = user_id_list
        else:
            follow_list = None
        if track_list:
            track_list = [k for k in track_list.split(',')]
        else:
            track_list = None
        stream.userstream(api, is_async=True)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
