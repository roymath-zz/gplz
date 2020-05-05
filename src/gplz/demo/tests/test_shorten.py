import pytest
from gplz.demo import shorten


def test_basic():
    shorten.clear()

    # basic functionality
    url = b"some/very/long/url?with-arg1=xx&arg2=yy"
    assert shorten.shorten(url)[0] == 'new'

    # test caching
    assert shorten.shorten(url)[0] == 'cached'

    # basic functionality with a second url; test caching
    url2 = b"some/other/url?with-arg1=abb&arg2=yy"
    assert shorten.shorten(url2)[0] == 'new'
    assert shorten.shorten(url2)[0] == 'cached'

    # create a custom short code
    url3 = b"/my/custom/url/one?arg1=x1&arg2=x2"
    assert shorten.custom(url3, 'custom1') == ('new', 'custom1')

    # don't reuse custom short codes
    with pytest.raises(Exception, match='already exists'):
        assert shorten.custom(url3, 'custom1')

    # don't allow invalid custom short codes
    with pytest.raises(Exception, match='invalid characters in shortcode'):
        assert shorten.custom(url3, '?custom1')

    # allow multiple shortcodes to reference the same url
    assert shorten.custom(url3, 'custom2') == ('new', 'custom2')

    # test lookup of short codes
    assert shorten.lookup('custom1')['url'] == url3

    # test attributes of short codes
    assert shorten.lookup('custom1')['access_count'] == 2
    assert shorten.lookup('custom1')['created']

    # negative test
    with pytest.raises(Exception, match='no sha'):
        assert shorten.lookup('junk')

    # clear cache; make sure we get a new short code.
    shorten.clear()
    assert shorten.shorten(url)[0] == 'new'
