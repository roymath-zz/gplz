import hashlib
import urllib.parse
import datetime
import base64
from pprint import pprint
import string
import random
random.seed('x')

URLLEN = 10  # max chars in shortened url
CHOICES = string.printable[:62]  # select only digits and letters
"""
maintain a lookup table of:
  _cache = {sha: {url, shortcode, created, access_count}}

and a set of shortcodes for reverse lookup
  _shortcodes = {shortcode: sha}
"""

_cache = {}
_shortcodes = {}


def new_shortcode():
    while True:
        shortcode = ''.join([random.choice(CHOICES) for e in range(URLLEN)])
        if shortcode not in _shortcodes:
            return shortcode


def shorten(url):
    m = hashlib.sha256()
    m.update(url)
    sha = m.digest()

    if sha in _cache:
        return 'cached', _cache[sha]['shortcode']

    # need new short-code; generate and add to cache
    shortcode = new_shortcode()
    ts = datetime.datetime.now().timestamp()
    _cache[sha] = {'shortcode': shortcode, 'url': url, 'created': ts}
    _shortcodes[shortcode] = sha

    return 'new', shortcode


def lookup(shortcode):
    try:
        sha = _shortcodes[shortcode]
        res = _cache[sha]
        res.setdefault('access_count', 0)
        res['access_count'] += 1
        return res
    except:
        raise Exception(f'no sha found in {"/".join(list(_shortcodes))}')


# clear global cache (for testing)
def clear():
    global _cache
    global _shortcodes
    _cache, _shortcodes = {}, {}

