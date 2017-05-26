import sys
import json
from urlparse import urlparse


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
    def __init__(self, headers={}, body='', status_code=200):
        self.headers = headers
        self.body = body
        if not isinstance(self.body, basestring) \
                and not isinstance(self.body, dict) \
                and not isinstance(self.body, list):
            self.body = str(self.body)
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
