#!/usr/bin/env python

import re
import httplib2
import urllib
import urllib.request as request
import json

from lib import exception
from googletrans import Translator
from queue import Queue
from threading import Thread
from datetime import datetime
from pytz import utc
from bs4 import UnicodeDammit


global_meta_args = {}

class scraper_handler:
	__metaclass__ = exception.ErrorCatcher
	meta_args = global_meta_args
	def __init__(self, handlers):
		self.handlers = handlers

	def check(self, data):
		results = {}
		for regex in self.handlers:
			key = regex
			regex = re.compile(regex, re.IGNORECASE)
			search = regex.findall(data)
			if search:
				result = self.handlers[key](search)
				results.update(result)
		return results


class handlers:
	__metaclass__ = exception.ErrorCatcher
	meta_args = global_meta_args
# handlers take search data and return a dict for json processing
###############################################################################

	def __init__(self):
		self.card_handlers = {
			r"\b[0-9]{16}\b": self.ccn_handler,
			r"\b(APPROVED|DECLINED|APROVADA|RECUSOU|REPROVADO|DECLINE)\b":
				lambda x: {"card_status": [y.lower() for y in x]},

			r"\b[0-9]{1,2}.[0-9]{2}(?=\$)\b": lambda x: {"card_charge": x},
			r"\b[0-9]{1,2}.[0-9]{2}(?= R\$)\b": lambda x: {"card_charge": x},
			r"\b(DEBIT|CREDIT)\b": lambda x: {"card_account": [y.lower() for y in x]},

			r"\b(CLASSIC|STANDARD|PLATINUM|BUSINESS|WORLD CARD|GOLD|TITANIUM|"
			r"CENTURION|ELECTRON|CORPORATE|PREPAID|SIGNATURE|"
			r"CORPORATE PURCHASING|INFINITE)\b": lambda x: {"card_class": [y.lower() for y in x]}
		}

		self.darknet_handlers = {
			r".*([a-z2-7]{16}\.onion)": lambda x: {"darknet_onion": [y.lower() for y in x]},
		}

		self.pastebin_handlers = {
			r"\bhttps?://pastebin\.com/[A-Z0-9]{8}\b":
				self.pastebin_to_raw_handler,
			r"\bhttps?://pastebit\.co/[A-Z0-9]{8}\b":
				self.pastebin_to_raw_handler,
			r"\bhttps?://pastebit\.co/raw/[A-Z0-9]{8}\b":
				self.generic_pastebin_handler,
			r"\bhttps?://pastebin\.com/raw/[A-Z0-9]{8}\b":
				self.generic_pastebin_handler,
			r"\bhttps?://sprunge\.us/[A-Z0-9]{4}\b":
				self.generic_pastebin_handler,
		}

		self.contact_handlers = {
			r"(\b[A-Z0-9_.+-]+@[A-Z0-9-]+\.[A-Z0-9-.]+(?!IP)\b)":
				lambda x: {"contact_email": [y.lower() for y in x]},
		}

		self.web_handlers = {
			r"(?:http|ftp|git|irc)s?://"
			r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
			r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?(?:/?|[/?]\S+)":
				lambda x: {"web_site": [y.lower() for y in x]},
			r"(?:http|ftp|git|irc)s?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|"
			r"(?:%[0-9a-fA-F][0-9a-fA-F]))+": lambda x: {"web_link": x},
			r"(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})":
				lambda x: {"web_ip": x},
			r"(?:https?://music\.youtube\.com/watch\?v=.*)": lambda x: {"youtube-music": x},
			r"(?:https?://youtube\.com/watch\?v=.*)": lambda x: {"youtube": x}
		}
		
		self.action_handlers = {
			"youtube": self.youtube_handler,
			"youtube-music": self.youtube_handler
		}
		self.scrapers = [
			scraper_handler(self.card_handlers),
			scraper_handler(self.darknet_handlers),
			scraper_handler(self.pastebin_handlers),
			scraper_handler(self.contact_handlers),
			scraper_handler(self.web_handlers),
		]
		self.queue = Queue()
		self.thread = Thread(target=self.worker)
		self.thread.daemon = True
		self.thread.start()

	def worker(self):
		while True:
			try:
				cself, src, dst, prefix, command, arguments, text = self.queue.get()
				body = {
					"server": "irc%s://%s:%s" % (
						's' if cself.ssl else '',
						cself.server, cself.port),
					"src": src.lower(),
					"dst": dst.lower() if dst != cself.nick else '@pm',
					"prefix": prefix,
					"@timestamp": datetime.now(tz=utc).isoformat(),
					"message_text": UnicodeDammit(text).unicode_markup,
					"raw": "%s %s %s" % (prefix, command, arguments)
				}
				# https://music.youtube.com/watch?v=uC6wKP_RVqU
				# https://www.youtube.com/oembed?url=https://music.youtube.com/watch?v=uC6wKP_RVqU&si=ev2BqzOZ3YGFB9b1
				result = self.is_screened(text)
				if result:
					print("Found: %s" % result)
					for k in result.keys():
						if k in self.action_handlers:
							self.action_handlers[k](cself, src, dst, result[k])
					
			except Exception as e:
				print("!!!!!!!!!!!!!!!!!! %s !!!!!!!!!!!!!!!!!!" % e)
				continue

	def youtube_handler(self, cself, src, dst, data):
		link = data[0]
		title = None
		author = None
		
		lookup = "https://www.youtube.com/oembed?%s" % (urllib.parse.urlencode({"url": data[0]}))
		with request.urlopen(lookup) as response:
			response_text = response.read()
			data = json.loads(response_text.decode())
			print(data)
			# 00[ 09youtube 12| 00title: 09%s 12| 00author: 09%s 12]
			cself.privmsg(dst, "04[00 youtube 04❤️00 title: %s 04❤️00 author: %s 04]" % (data["title"], data["author_name"]))

	def handle(self, cself, src, dst, prefix, command, arguments, text):
		self.queue.put([cself, src, dst, prefix, command, arguments, text])
		
	def is_screened(self, data):
		results = {}
		for scraper in self.scrapers:
			result = scraper.check(data)
			results.update(result)
		return results

	def lang_detect(self, text):
		translator = Translator()
		return translator.detect(text).lang

#	def translate(self, text):
#		try:
#			results = {}
#			translator = Translator()
#			lang = self.lang_detect(text)
#			if lang != 'en':
#				results["translation"] = {}
#				results["translation"]["data"] = \
#					translator.translate(text, dest='en').text.encode('utf-8')
#				results["translation"]["lang"] = lang
#			else:
#				return None
#			return results
#		except:
#			return None


	def ccn_handler(self, search):
		def neo_handler(tx, job):
			res = tx.run(job)
			# we only need the first result
			for r in res:
				res = r
				break
			r = {}
			if "Scheme" in res:
				r.update({"Scheme": res["Scheme"]})
			if "Bank" in res:
				r.update({"Bank": res["Bank"]})
			if "Country" in res:
				r.update({"Country": res["Country"]})
			print(r)
			return r
		def bin_lookup(x):
			results = {"card": x}
			## query neo4j and return all relevent card information
			########################################################
			neo_result = neo4j.graph_handler('match (a:Bin:Number)--(b:Bin:Scheme) where a.name = "%s" optional match (a:Bin:Number)--(c:Bin:Bank) optional match (a:Bin:Number)--(d:Geo:Country) return b.name as Scheme, c.name as Bank, d.geohash as Country' % x[:6],
								"10.100.90.221", "neo4j", "62b78c0dff", neo_handler, read=True)
			results.update(neo_result)
			return results
		def luhn(n):
			r = [int(ch) for ch in str(n)][::-1]
			return (sum(r[0::2]) + sum(sum(divmod(d*2,10)) for d in r[1::2])) % 10 == 0
		r = [bin_lookup(x) for x in search if luhn(x)]
		r = [x for x in r if x]
		print(r)
		return {"card_ccn": r} if r else {}

	def generic_pastebin_handler(self, search):
		results = {}
		results["pastebin"] = {}
		results["pastebin"]["raw"] = []

		h = Http(".cache", disable_ssl_certificate_validation=True)
		for result in search:
			resp, content = h.request(
				result, "GET", headers={'content-type': 'text/plain'})
			results["pastebin"]["raw"].append((result, content))
#			trans = self.translate(content)
#			if trans:
#				if "translated" not in results["pastebin"]:
#					results["pastebin"]["translated"] = []
#				trans["site"] = result
#				results["pastebin"]["translated"].append(trans)
			results.update(self.is_screened(content))
		return results

	def pastebin_to_raw_handler(self, search):
		search2 = []
		for result in search:
			search2.append(re.sub(
				r".com/(?<!raw)",
				r".com/raw/",
				result, flags=re.IGNORECASE))
		return generic_pastebin_handler(search2)
