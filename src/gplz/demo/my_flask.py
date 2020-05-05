import json
import logging

from flask import Flask, Response, redirect, url_for
from flask import request
from flask import make_response
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from gplz.demo import shorten

demo = Flask(__name__)
demo.config.from_object('flask_config')
CORS(demo)

logging.getLogger('flask_cors').level = logging.DEBUG

# @demo.errorhandler(Exception)
# def handle_exception(e):
#     # pass through HTTP errors
#     if isinstance(e, HTTPException):
#         return e

#     # now you're handling non-HTTP exceptions only
#     return Response(str(e), 500)

@demo.route('/')
def get():
    res = make_response('ho yo')
    res.add_etag()
    return res

@demo.route('/ops/shorten', methods=['POST'])
def handle_shorten():
    data = request.get_json()
    url = data.get('url', 'NO URL')
    res = shorten.shorten(url.encode('utf8'))
    return Response(json.dumps(res), mimetype='application/json')


@demo.route('/ops/custom', methods=['POST'])
def handle_custom():
    data = request.get_json()
    url = data.get('url', 'NO URL')
    shortcode = data.get('shortcode', 'NO SHORTCODE')
    res = shorten.custom(url.encode('utf8'), shortcode)
    return Response(json.dumps(res), mimetype='application/json')


@demo.route('/ops/lookup', methods=['POST'])
def handle_lookup():
    data = request.get_json()
    url = data.get('shortcode', 'NO URL')
    res = shorten.lookup(url)
    return Response(json.dumps(res['url'].decode('utf8')), mimetype='application/json')

@demo.route('/<path>', methods=['GET'])
def handle_redirect(path):
    res = shorten.lookup(path)
    url = res['url'].decode('utf8')
    return redirect(url)
    # return Response(json.dumps(path), mimetype='application/json')


if __name__ == "__main__":
    demo.run()

