# file is automatically picked up by pytest; declare fixtures here

import random
import json

from pytest import fixture

from gplz.demo import shorten

@fixture(scope='class')
def clearCache():
    shorten.clear()

@fixture(scope='module', name='mockEvents')
def getMockEvents():
    pass

