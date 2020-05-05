import unittest
import json

from gplz.demo import my_flask

demo = my_flask.demo.test_client()


class TestFlaskOps:
    def makeRequest(self):
        response = demo.post(
            '/ops/shorten',
            json={'url': 'https://google.com?q=flowers&s=lilacs'},
            follow_redirects=True,
            headers={"Content-Type": "application/json"},
        )
        return response

    def test_get(self):
        response = demo.get('/')
        data = response.data.decode("utf-8")
        assert data == "ho yo"
        etag = json.loads(response.headers['etag'])
        assert etag == "9031b4bb342abf3270d8ffc9e1ead3de"

    def test_shorten(self):
        response = self.makeRequest()
        assert response.headers['Content-Type'] == 'application/json'
        data = response.get_json()
        assert data == ['new', 'EkCCu4MWoB']

    def test_lookup(self, clearCache):
        response = self.makeRequest()  # prime the cache

        response = demo.post(
            '/ops/lookup',
            json={'shortcode': 'tGsoaoYuAO'},
            follow_redirects=True,
            headers={"Content-Type": "application/json"},
        )
        assert response.headers['Content-Type'] == 'application/json'
        data = response.get_json()
        assert data == 'https://google.com?q=flowers&s=lilacs'

    def test_redirect(self, clearCache):
        response = self.makeRequest()  # prime the cache

        response = demo.get(
            '/EkCCu4MWoB',
            follow_redirects=True,
            headers={"Content-Type": "application/json"},
        )
        assert response.headers['Content-Type'] == 'application/json'
        data = response.get_json()
        assert data == 'https://google.com?q=flowers&s=lilacs'


