#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from time import time
from hashlib import sha256
from lib import irc_callbacks

#self.authed = {
#	"heather!heather@D600793F.C4E730A4.CF975CBA.IP": time()
#}
## echo -n "password" | sha256sum -
#self.mods = {
#	"heather": "6cd1dbcb7abb51dd132c67d9510ac309e25f573e874570b790856149878c60a0"
#}

def is_authed(cself, prefix, perm):
	if prefix not in cself.authed.keys():
		return False
	is_perm = False
	for p in perm:
		is_perm ^= (cself.authed[prefix][0] in p)
	return (time() - cself.authed[prefix][1]) < 86400 and is_perm

def authenticate(cself, src, dst, prefix, user, password):
	hashpass = sha256(password.encode()).hexdigest()
	print(hashpass, cself.mods[user][1])
	if user in cself.mods and hashpass == cself.mods[user][1]:
		cself.authed[prefix] = (cself.mods[user][0], time())
		
		irc_callbacks.respond(cself, src, dst, "You are now authenticated :)")
		for chan in cself.channels:
			cself.mode(chan, "+%s %s" % (cself.mods[user][0], src))
	else:
		irc_callbacks.respond(cself, src, dst, "Nice try ;)")
	
