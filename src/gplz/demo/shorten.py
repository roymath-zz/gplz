"""
maintain a lookup table of:
  _cache = {sha: {url, shortcode, created, access_count}}

and a set of shortcodes for reverse lookup
  _shortcodes = {shortcode: sha}
"""

from urllib.parse import urlparse
import hashlib
import datetime
import string
import random

random.seed('x')  # predictable test values

URLLEN = 10  # max chars in shortened url
CHOICES = string.printable[:62]  # select only digits and letters

_cache = {}
_shortcodes = {}


# helper: generate new shortcode
def new_shortcode():
    while True:
        shortcode = ''.join([random.choice(CHOICES) for e in range(URLLEN)])
        if shortcode not in _shortcodes:
            return shortcode


# helper: create new sha
def new_sha(url):
    m = hashlib.sha256()
    m.update(url.encode('utf8'))
    sha = m.digest()
    return sha


def check_url(url):
    res = urlparse(url)
    if not res.scheme or not res.netloc:
        raise Exception(f'invalid url {url}')


# add entry in caches
def add(url, shortcode, sha):
    check_url(url)  # validate

    ts = datetime.datetime.now().timestamp()
    _cache[sha] = {
        'shortcode': shortcode,
        'url': url,
        'created': ts
    }
    _shortcodes[shortcode] = sha
    return 'new', shortcode


# shorten url
def shorten(url, custom=None):
    sha = new_sha(url)
    if sha in _cache:
        return 'cached', _cache[sha]['shortcode']

    # need new short-code; generate and add to cache
    shortcode = new_shortcode()
    return add(url, shortcode, sha)


# shorten url w/custom shortcode
def custom(url, shortcode):
    if shortcode in _shortcodes:
        raise Exception(f'shortcode {shortcode} already exists!')
    if len(set(shortcode) - set(CHOICES)):
        raise Exception(f'invalid characters in shortcode {shortcode}!')

    # prefix the url with the custom shortcode to allow multiple refs
    sha = new_sha(f'{shortcode}: {url}')

    return add(url, shortcode, sha)


# lookup url by shortcode
def lookup(shortcode):
    try:
        sha = _shortcodes[shortcode]
        res = _cache[sha]
        res.setdefault('access_count', 0)
        res['access_count'] += 1
        return res
    except Exception:
        raise Exception(f'no sha found in {"/".join(list(_shortcodes))}')


# dump all cached data
def dump():
    return _cache.values()


# clear global cache (for testing)
def clear():
    global _cache
    global _shortcodes
    _cache, _shortcodes = {}, {}
