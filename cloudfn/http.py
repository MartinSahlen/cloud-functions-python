import json
import sys

import six
from six.moves.urllib_parse import urlparse


class Request:
    def __init__(self, raw_json):
        self.headers = raw_json['headers']
        self.method = raw_json['method']
        self.body = raw_json['body']
        self.url = raw_json['url']
        self.ip = raw_json['remote_addr']

        components = urlparse(self.url)
        self.path = components.path
        self.host = components.hostname
        self.scheme = components.scheme
        self.query = components.query
        self.port = components.port
        self.fragment = components.fragment
        self.params = components.params
        self.netloc = components.netloc


class Response:
    def __init__(self, headers=None, body='', status_code=200):
        self.headers = {} if headers is None else headers
        if isinstance(body, (six.text_type, six.binary_type, dict, list)):
            self.body = body
        else:
            self.body = str(body)
        self.status_code = status_code

    def _json_string(self):
        return json.dumps({
            'body': self.body,
            'status_code': self.status_code,
            'headers': self.headers,
        })


def handle_http_event(handle_fn):
    req = Request(json.loads(sys.stdin.read()))
    res = handle_fn(req)
    if isinstance(res, Response):
        sys.stdout.write(res._json_string())
    else:
        sys.stdout.write(Response()._json_string())
