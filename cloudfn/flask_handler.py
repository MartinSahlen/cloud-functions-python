import json
import sys
from io import StringIO

import six
from six.moves.urllib_parse import urlparse
from werkzeug.datastructures import Headers

# from .wsgi_util import wsgi


def handle_http_event(app):
    req_json = json.loads(sys.stdin.read())
    c = urlparse(req_json['url'])
    path = c.path
    if path == '':
        path = '/'

    body = StringIO(req_json.get('body', u''))

    req_headers = req_json.get('headers', None)
    h = Headers()
    if req_headers is not None:
        for key, value in six.iteritems(req_headers):
            h.add(key, value)

    with app.test_request_context(
            path=path,
            input_stream=body,
            method=req_json.get('method', 'GET'),
            headers=h,
            query_string=c.query):
        resp = app.full_dispatch_request()
        body = resp.get_data()
        try:
            body = json.loads(body)
        except:
            pass

        headers = {}
        for header in resp.headers:
            if header[0] in headers:
                headers[header[0]] += ', ' + header[1]
            else:
                headers[header[0]] = header[1]

        sys.stdout.write(json.dumps({
            'body': body,
            'status_code': resp.status_code,
            'headers': headers,
        }))
