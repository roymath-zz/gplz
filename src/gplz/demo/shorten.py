import hashlib
import urllib.parse
import base64
from pprint import pprint
import string
import random
random.seed('x')

URLLEN = 10  # max chars in shortened url
CHOICES = string.printable[:62]  # select only digits and letters
"""
maintain a lookup table of:
  {sha: {url, shortcode}}

and a set of shortcodes for reverse lookup
  {shortcode: sha}
"""

_cache = {}
_shortcodes = {}


def new_shortcode():
    while True:
        shortcode = ''.join([random.choice(CHOICES) for e in range(URLLEN)])
        if shortcode not in _shortcodes:
            return shortcode


def lookup(shortcode):
    try:
      sha = _shortcodes[shortcode]
      return _cache[sha]
    except:
      raise Exception(f'no sha found in {"/".join(list(_shortcodes))}')

# clear global cache (for testing)
def clear():
    global _cache
    global _shortcodes
    _cache, _shortcodes = {}, {}


def shorten(url):
    m = hashlib.sha256()
    m.update(url)
    sha = m.digest()

    if sha in _cache:
        return 'cached', _cache[sha]['shortcode']

    # need new short-code; generate and add to cache
    shortcode = new_shortcode()
    _cache[sha] = {'shortcode': shortcode, 'url': url}
    _shortcodes[shortcode] = sha

    return 'new', shortcode

