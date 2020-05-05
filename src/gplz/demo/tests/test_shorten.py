import pytest
from gplz.demo import shorten

def test_basic():
  url = b"some/very/long/url?with-arg1=xx&arg2=yy"
  assert shorten.shorten(url) == ('new', 'EkCCu4MWoB')
  assert shorten.shorten(url) == ('cached', 'EkCCu4MWoB')

  url2 = b"some/other/url?with-arg1=abb&arg2=yy"
  assert shorten.shorten(url2) == ('new', 'tGsoaoYuAO')
  assert shorten.shorten(url2) == ('cached', 'tGsoaoYuAO')

  assert shorten.lookup('tGsoaoYuAO')['url'] == url2
  with pytest.raises(Exception, match='no sha'):
    assert shorten.lookup('junk')

  shorten.clear()
  assert shorten.shorten(url)[0] == 'new'
