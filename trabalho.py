#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Captura tweets mundiais dos trending topics, desenha o mapa mundi e então plota pontos a partir das coordenadas de cada tweet (quando disponíveis) """

import datetime
from threading import Timer

# Mapa
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
# Mensagem de erro
from tkMessageBox import showerror
# sys.exit()
import sys
# Twitter
from twitter import *
import tweepy

CONFIG_MAP_PATH_TO_FILE = "map.ini"
CONFIG_TWITTER_PATH_TO_FILE = "twitter.ini"

class Config:
	""" Desserializa um arquivo de configuração genérico do tipo "NOME_CONFIG=VALOR_CONFIG;NOME_CONFIG=VALOR_CONFIG" """
	def __init__(self, config_file):
		self.__config = self.__read_config_file(config_file)

	def __read_config_file(self, config_file):
		file_content = ''
		config = {}
		try:
			with open(config_file, "r") as file:
				file_content = file.read().split(";")
				for line in file_content:
					config_line = line.split("=")
					config[config_line[0]] = config_line[-1]
			return config
		except IOError:
			showerror("I/O error", "Couldn't open file {}".format(config_file))
			sys.exit(1)

	def get_config(self, config_key):
		try:
			return self.__config[config_key]
		except KeyError:
			showerror("Config key", "Config key {} not found".format(config_key))
			sys.exit(1)

class Map:
	""" Gerencia o desenho do mapa e pontos na tela """
	def __init__(self, config_file="map.ini"):
		self.__config = Config(config_file)
		self.map = Basemap(projection=self.__config.get_config("PROJECTION"), resolution=self.__config.get_config("RESOLUTION"), lon_0=0)
		self.map.drawcoastlines()
		self.map.drawmapboundary(fill_color=self.__config.get_config("OCEAN_COLOR"))
		self.map.fillcontinents(color=self.__config.get_config("CONTINENT_COLOR"), lake_color=self.__config.get_config("LAKE_COLOR"))
		plt.ion()

	def plot_point(self, lat, lon, radius):
		x, y = self.map(lon, lat)
		self.map.plot(x, y, 'bo', markersize=radius)

class AuthHandler:
	""" Responsável pelo processo de autenticação do Twitter """
	def __init__(self, config_file="twitter.ini"):
		self.connected = False
		self.__config = Config(config_file)
		self.__auth = tweepy.OAuthHandler(self.__config.get_config("CONSUMER_KEY"), self.__config.get_config("CONSUMER_SECRET"))
		self.twitter = Twitter(auth = OAuth(self.__config.get_config("ACCESS_TOKEN"), self.__config.get_config("ACCESS_TOKEN_SECRET"), self.__config.get_config("CONSUMER_KEY"), self.__config.get_config("CONSUMER_SECRET")))
		self.__auth.set_access_token(self.__config.get_config("ACCESS_TOKEN"), self.__config.get_config("ACCESS_TOKEN_SECRET"))
		self.api = tweepy.API(self.__auth)
		self.connected = True

class TrendsStreamListener(tweepy.StreamListener):
	def __init__(self, auth_handler):
		self.api = auth_handler.api
		self.twitter = auth_handler.twitter
		self.trends_round = 0
		self.map = Map(CONFIG_MAP_PATH_TO_FILE)
		self.stream = tweepy.Stream(auth=self.api.auth, listener=self)
		self.get_new_trends()
		self.__set_timer()
	
	def get_new_trends(self):
		self.trends_round += 1
		trends_json = self.api.trends_place(id=1)
		trends_data = trends_json[0]
		trends = trends_data['trends']
		trends_name = [trend['name'] for trend in trends]
		print trends_name
		self.stream.filter(track=trends_name, async=True)
		#t = self.twitter.tweets(q='#python')
		#print t

	def __set_timer(self):
		self.__timer = Timer(30, self.redraw_map)
		self.__timer.start()

	def redraw_map(self):
		plt.draw()
		self.__timer.stop()
		self.__set_timer()

	def on_status(self, tweet):
		if (tweet.coordinates != None):
			print tweet.coordinates
			self.map.plot_point(tweet.coordinates['coordinates'][1], tweet.coordinates['coordinates'][0], 5)
			plt.pause(1)
			
	def on_error(self, status):
		print ("[" + str(datetime.datetime.now()) + "] " + str(status))

# Apenas essa linha é executada enquanto o mapa está aberto
"""MY_MAP = Map()"""

"""# Linhas abaixos são executadas somente depois de se fechar o mapa
MY_AUTH_HANDLER = AuthHandler()
MY_MAP.plot_point(-33.924869, 18.424055, 5)
print MY_AUTH_HANDLER.connected"""

MY_AUTH_HANDLER = AuthHandler()
TRENDS_STREAM_LISTENER = TrendsStreamListener(MY_AUTH_HANDLER)
