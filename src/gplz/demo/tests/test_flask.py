import pytest
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

    def test_shorten(self):
        response = self.makeRequest()
        assert response.headers['Content-Type'] == 'application/json'
        data = response.get_json()
        assert data == ['new', 'EkCCu4MWoB']

    def test_custom(self):
        response = demo.post(
            '/ops/custom',
            json={
                'url': 'https://google.com?q=flowers&s=lilacs',
                'shortcode': 'custom1',
            },
            follow_redirects=True,
            headers={"Content-Type": "application/json"},
        )
        assert response.headers['Content-Type'] == 'application/json'
        data = response.get_json()
        assert data == ['new', 'custom1']

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

    def test_dump(self, clearCache):
        response = self.makeRequest()  # prime the cache

        response = demo.get('/ops/dump')
        assert response.headers['Content-Type'] == 'application/json'
        data = response.get_json()
        assert data[0]['url'] == 'https://google.com?q=flowers&s=lilacs'

    @pytest.mark.skip(reason="flask testing: issue w/external redirects")
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
