# from wsgi_util import wsgi
import json
import sys
from urlparse import urlparse
from io import StringIO
from werkzeug.datastructures import Headers

# http://werkzeug.pocoo.org/docs/0.12/test/#werkzeug.test.EnvironBuilder
# to build the full request


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
        for key, value in req_headers:
            h.add(key, value)

    with app.test_request_context(
            path=path,
            input_stream=body,
            method=req_json['method'],
            headers=h,
            query=c.query):
        resp = app.full_dispatch_request()
        body = resp.get_data()
        try:
            body = json.loads(body)
        except:
            pass

        headers = {}
        for header in resp.headers:
            if header[0] in headers:
                headers[header[0]] = headers[header[0]] + ', ' + header[1]
            else:
                headers[header[0]] = header[1]

        sys.stdout.write(json.dumps({
            'body': body,
            'status_code': resp.status_code,
            'headers': headers,
        }))
