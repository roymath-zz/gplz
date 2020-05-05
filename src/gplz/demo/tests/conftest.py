# file is automatically picked up by pytest; declare fixtures here

from pytest import fixture

from gplz.demo import shorten


@fixture(scope='class')
def clearCache():
    shorten.clear()
