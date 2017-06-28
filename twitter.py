# -*- encoding:utf-8 -*-
import tweepy
import time

""" 
API.trends_place(id=1) -> pega os trending topics mundiais
"""

CONSUMER_KEY = ""
CONSUMER_SECRET = ""

ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

API = tweepy.API(AUTH)

TRENDS_WORLD = API.trends_place(id=1)

DATA = TRENDS_WORLD[0]

TRENDS = DATA['trends']

NAMES = [trend['name'] for trend in TRENDS]

#TRENDS_NAME = ' '.join(NAMES)
#print TRENDS_NAME
	


class TrendsStreamListener(tweepy.StreamListener):
	def on_status(self, tweet):
		print tweet.text
		
TRENDS_STREAM_LISTENER = TrendsStreamListener(API)
TRENDS_STREAM = tweepy.Stream(auth=API.auth, listener=TRENDS_STREAM_LISTENER)
TRENDS_STREAM.filter(track=NAMES)
