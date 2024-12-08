#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from time import sleep
from json import load
#from thread import start_new_thread
import threading

from lib import irc
from lib import irc_callbacks
from lib import exception


class irc_connection:
	__metaclass__ = exception.ErrorCatcher
	
	def __init__(self, prefix, server, channels, callbacks, port, sslflag, mods):
		self.thread = None
		self.kill_signal = None
		
		self.bot = irc.Bot(self.kill_signal, prefix, server, port, sslflag, channels, mods)
		self.bot.callbacks.update(callbacks)

	def run(self):
		while not self.kill_signal.is_set():
			try:
				self.bot.connect()
				if self.bot.socket:
					self.bot.register()
					self.bot.consume()
			except:
				print("connection failed... retrying")
				self.kill_signal.set()


def load_config():
	with open("./config.json") as f:
		config = load(f)
	return config

kill_signal = threading.Event()
connections = []

def start_threads():
	config = load_config()
	callbacks = irc_callbacks.irc_callbacks()
	
	for server in config:
		connection = irc_connection(config[server]["prefix"], server,
			config[server]["channels"],
			callbacks.callbacks,
			6697 if "port" not in config[server]
				else config[server]["port"],
			True if "sslflag" not in config[server]
				else config[server]["sslflag"], {} if "mods" not in config[server] else config[server]["mods"])
		
		connections.append(connection)
		connection.thread = threading.Thread(target=connection.run)
		connection.kill_signal = kill_signal
		connection.thread.start()
		

def kill_threads():
	for connection in connections:
		connection.kill_signal.set()
		connection.thread.join()
	connections = []



