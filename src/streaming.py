'''
streaming.py by Jaime Hisao Yesaki 
Program that connects to the Twitter API and streams tweets instead of querying them in timely intervals.
Created September 3, 2019
Version 0.1
'''
import sys
from src.config import create_api
from tweepy import Stream
from tweepy.streaming import StreamListener


class Listener(StreamListener):
    def __init__(self, output_file=sys.stdout):
        super(Listener, self).__init__()
        self.output_file = output_file

    def on_status(self, status):
        print(status.text, file=self.output_file)

    def on_error(self, status_code):
        print(status_code)
        return False


api = create_api()

output = open('stream_output.txt', 'w')
listener = Listener(output_file=output)

stream = Stream(auth=api.auth, listener=listener)
try:
    print('Start streaming.')
    stream.sample(languages=['en'])
except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    print('Done.')
    stream.disconnect()
    output.close()
