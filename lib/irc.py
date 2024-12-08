#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import ssl
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from time import time
import re

from bs4 import UnicodeDammit
from ftfy import fix_encoding

from lib import exception


global_meta_args = {}

def ping_callback(self, prefix, command, arguments):
	self.pong(arguments)


class Bot:
	__metaclass__ = exception.ErrorCatcher
	meta_args = global_meta_args

	def __init__(self, kill_signal, usermask, server,
				 port=6667, sslflag=False,
				 channels=None, mods={}):
		self.kill_signal = kill_signal
		self.usermask = usermask
		self.server = server
		self.port = port
		self.ssl = sslflag
		self.socket = None

		self.nick = usermask.split('!')[0]
		self.user, self.host = usermask.split('!')[1].split('@')

		self.channels = channels
		self.callbacks = {}
		self.authed = {
			#"heather!heather@D600793F.C4E730A4.CF975CBA.IP": ("o",time())
		}
		# echo -n "password" | sha256sum -
		self.mods = mods

	def handle_formatting(self, line):
		# strip colors
		line = re.sub("(\x03[0-9]{1,2},[0-9]{1,2})|(\x03[0-9]{1,2})|\x03", "", line)
		
		# strip special formatting
		line = re.sub("\x02|\x1D|\x1F|\x16|\x0F", "", line)
		
		# strip ACTION
		line = re.sub("(\x01ACTION )|\x01", "", line)
		
		return line
	def consume(self):
		print("Consume...")
		reader = self.socket.makefile("r")
		while self.socket:
			try:
				line = reader.readline()
				line = fix_encoding(line.rstrip('\r\n'))
	
				line = self.handle_formatting(line)
				print(line)
				line = line.split(' ')
				# remove later
				prefix = line[0][1:] if line[0][0] == ':' else None
				command = (line[1] if prefix is not None else line[0]).upper()
				arguments = ' '.join(
					line[2:] if prefix is not None else line[1:])
			except:
				print("exception in consume")

			if command in self.callbacks:
				self.callbacks[command](self, prefix, command, arguments)

	def connect(self):
		print("Connect...")
		try:
			s = socket(AF_INET, SOCK_STREAM)
			s.settimeout(10)
			if self.ssl:
				self.socket = ssl.wrap_socket(s)
			else:
				self.socket = s
			self.socket.connect((self.server, self.port))
			s.settimeout(300)
		except Exception as e:
			print("exception in connect", e)
			self.socket = None
			raise

		return self.socket

	def disconnect(self):
		return self.socket.close()


	def change_nick(self, nick):
		self.nick = nick
		buf = "NICK %s\r\n" % self.nick
		self.socket.send(buf.encode())
	
	def register(self):
		buf = "USER %s 0 * :%s\r\n" % (self.user, self.user)
		self.socket.send(buf.encode())
		self.change_nick(self.nick)

	def join(self, chan):
		buf = "JOIN %s\r\n" % chan
		self.socket.send(buf.encode())
		
		self.privmsg(chan, "That's QUEEN bot to you BuD!")
	
	def kick(self, chan, nick, message):
		buf = "KICK %s %s :%s\r\n" % (chan, nick, message)
		self.socket.send(buf.encode())

	def privmsg(self, dest, message):
		buf = "PRIVMSG %s :%s\r\n" % (dest, message)
		self.socket.send(buf.encode())
	
	def mode(self, chan, data):
		buf = "MODE %s %s\r\n" % (chan, data)
		
		self.socket.send(buf.encode())
		



