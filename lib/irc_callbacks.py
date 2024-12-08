#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from lib import exception
from lib import gather
from lib import auth
from lib import threads

from time import sleep, time
from datetime import datetime
from pytz import utc

import re

def respond(cself, src, dst, data):
	if dst[0] == "#":
		cself.privmsg(dst, "%s: %s" % (src, data))
	else:
		cself.privmsg(src, "%s" % (data))

def command_scrub(data):
	return [e for e in data.split(" ") if e != "" ]


def command_reload(cself, src, dst, prefix, data):
	if auth.is_authed(cself, prefix, "o"):
		respond(cself, src, dst, "Reloading, please wait :)")
		cself.disconnect()
		threads.kill_threads()
	else:
		respond(cself, src, dst, "That's MY purse, I don't know you.")
		cself.kick(dst, src, "H e E y A h H!!!!")


def command_join(cself, src, dst, prefix, data):
	if auth.is_authed(cself, prefix, "ho"):
		cself.join(command_scrub(data)[1:][0])
	else:
		respond(cself, src, dst, "That's MY purse, I don't know you.")
		cself.kick(dst, src, "H e E y A h H!!!!")

def command_nick(cself, src, dst, prefix, data):
	if auth.is_authed(cself, prefix, "o"):
		cself.change_nick(command_scrub(data)[1:][0])
	else:
		respond(cself, src, dst, "DON'T TOUCH ME THERE, YOU'RE NOT MY UNCLE!!!")


def command_op(cself, src, dst, prefix, data):
	if auth.is_authed(cself, prefix, "o"):
		data = command_scrub(data)
		if dst[0] == "#":
			if len(data) == 2:
				data = " ".join(data[1:])
				print(dst, "+o %s" % data)
				cself.mode(dst, "+o %s" % data)
			else:
				respond(cself, src, dst, "$op <nick>")
		else:
			respond(cself, src, dst, "This command can only be used in a channel bud...")
	else:
		respond(cself, src, dst, "Nice try...")

def command_auth(cself, src, dst, prefix, data):
	if dst == cself.nick:
		data = command_scrub(data)[1:]
		if len(data) == 2:
			user = data[0]
			password = data[1]
			auth.authenticate(cself, src, dst, prefix, user, password)
		else:
			respond(cself, src, dst, "$auth <username> <password>")
	else:
		respond(cself, src, dst, "Please do not use this command anywhere but in a PM, please ask to have your password changed if needed.........")

def command_doom(cself, src, dst, prefix, data):
	for line in [
	"  ███████████████████████████",
	"  ███████▀▀▀░░░░░░░▀▀▀███████",
	"  ████▀░░░░░░░░░░░░░░░░░▀████",
	"  ███│░░░░░░░░░░░░░░░░░░░│███",
	"  ██▌│░░░░░░░░░░░░░░░░░░░│▐██",
	"  ██░└┐░░░░░░░░░░░░░░░░░┌┘░██",
	"  ██░░└┐░░░░░░░░░░░░░░░┌┘░░██",
	"  ██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██",
	"  ██▌░│███♥██▌░░░▐██♥███│░▐██",
	"  ███░│▐███▀▀░░▄░░▀▀███▌│░███",
	"  ██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██",
	"  ██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██",
	"  ████▄─┘██▌░░░░░░░▐██└─▄████",
	"  █████░░▐█─┬┬┬┬┬┬┬─█▌░░█████",
	"  ████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████",
	"  █████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████",
	"  ███████▄░░░░░░░░░░░▄███████",
	"  ██████████▄▄▄▄▄▄▄██████████",
	"  ███████████████████████████",
	"❤️ Doom dAh dOoM DoOm DoOm!!! ❤️" ]:
		respond(cself, src, dst, line)
		sleep(0.3)

def command_fuck(cself, src, dst, prefix, data):
	data = " ".join(command_scrub(data)[1:])
	for line in [
	"     .-.",
	"     | |",
	"    _| |_     ",
	"   |_| | |-.  ",
	"  /  '-| | |\\ ",
	" (   ___)'-' |",
	"  \\   \\     / ",
	"   \\       /  ",
	"    |     |   ",
	"YEAH FUCK %s" % (data.upper())]:
		respond(cself, src, dst, line)
		sleep(0.3)
	
class irc_callbacks:
	__metaclass__ = exception.ErrorCatcher
	meta_args = {}

	def __init__(self):
		self.commands = {
			r"\$reload": command_reload,
			r"\$join .*": command_join,
			r"\$nick .*": command_nick,
			r"\$op .*": command_op,
			r"\$auth .*": command_auth,
			r"(^d|.* d)o(o+)m.*": command_doom,
			r"fuck .*": command_fuck,
		}
		
		self.callbacks = {
			"PING": self.ping_callback,
			"PRIVMSG": self.message_callback,
			"MODE": self.mode_callback,
			"JOIN": self.join_callback,
			"QUIT": self.join_callback,
			"PART": self.join_callback,
			"376": self.eomotd_callback,
			"433": self.nick_taken_callback
		}
		self.gather = gather.handlers()


	# :Deal!ChkNet@SecureDeal MODE #ccpower +v cyb3rm
	def mode_callback(self, cself, prefix, command, arguments):
		args = arguments.translate({ord(c): None for c in ":\r\n"}).split(' ')
		if args[0] == cself.nick:
			return
		else:
			body = {
				"server": "irc%s://%s:%s" % (
					's' if cself.ssl else '',
					cself.server, cself.port),
				"src":	prefix.split('!')[0],
				"dst":	args[0] if not len(args) >= 3 else args[2],
				"prefix": prefix,
				"channel": args[0],
				"mode":	args[1],
				"@timestamp":   datetime.now(tz=utc).isoformat(),
				"raw": "%s %s %s" % (prefix, command, arguments)
			}

	# :supreme!~supreme@B755E08D.FF219451.AD0E895C.IP JOIN :#unix
	# :sad_!sad@7CDE4C2E.F8656930.9935B4D6.IP QUIT :ChkNet
	# :MadMouse_!ayool@B76DBF88.53ECB30D.92E0E4C5.IP PART #Mafia :
	def join_callback(self, cself, prefix, command, arguments):
		args = arguments.translate({ord(c): None for c in ":\r\n"}).split(' ')
		src = prefix.split('!')[0]
		dst = args[0]
		if src == cself.nick:
			return
		body = {
			"server": "irc%s://%s:%s" % (
				's' if cself.ssl else '',
				cself.server, cself.port),
			"src":	src,
			"prefix": prefix,
			"join_channel": args[0],
			"join_status":  command,
			"@timestamp":   datetime.now(tz=utc).isoformat(),
			"raw": "%s %s %s" % (prefix, command, arguments)
		}

		if command == "JOIN":
			sleep(5)
			if src in cself.mods.keys():
				cself.privmsg(dst, "%s: Welcome back ❤️" % src)
			else:
				cself.privmsg(dst, "%s: Hello :)" % src)
		
		elif command == "PART":
			body["join_message"] = " ".join(args[1:])
		elif command == "QUIT":
			body["join_message"] = arguments

		#self.elastic.log("10.1.90.201", "spygames/irclogs_rev_2", body)

	def eomotd_callback(self, cself, prefix, command, arguments):
		cself.privmsg("nickserv", "identify mclovin 62b78c0dff")
		sleep(5)
		for channel in cself.channels:
			cself.join(channel)

	def nick_taken_callback(self, cself, prefix, command, arguments):
		cself.nick = cself.nick + "_"
		cself.register()

	def ping_callback(self, cself, prefix, command, arguments):
		buf = ("PONG %s\r\n" % arguments)
		print(buf)
		cself.socket.send(buf.encode())
		

	def message_callback(self, cself, prefix, command, arguments):
		args = arguments.split(' ')
		dst = args[0]
		src = prefix.split('!')[0]
		text = " ".join(args[1:])[1:]
		result = self.gather.handle(cself, src, dst, prefix, command, arguments, text)
		
		for command in self.commands:
			if re.search(command, text, re.IGNORECASE):
				for i in re.findall(command, text, re.IGNORECASE):
					self.commands[command](cself, src, dst, prefix, i)




