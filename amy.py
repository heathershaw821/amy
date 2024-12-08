#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import importlib

from lib import exception
from lib import irc
from lib import nlp
from lib import stop_words
from lib import email
from lib import gather
from lib import irc_callbacks

from lib import threads
from time import sleep


while True:
	importlib.reload(threads)
	importlib.reload(exception)
	importlib.reload(irc)
	importlib.reload(nlp)
	importlib.reload(stop_words)
	importlib.reload(email)
	importlib.reload(gather)
	importlib.reload(irc_callbacks)

	threads.start_threads()
	while not threads.kill_signal.is_set():
		sleep(1)
	threads.kill_signal.clear()
	print("kill signal received")
	sleep(10)

