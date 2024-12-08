#!/usr/bin/env python

import re

from collections import Counter
from lib.stop_words import stop_words


def get_frequencies(content):
    try:
        words = re.findall(r'\w+', content.lower())
        return Counter(words)
    except Exception as e:
        print("!!! get frequencies: %s" % e)
        return None





