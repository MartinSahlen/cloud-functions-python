import json
import sys

from django.core.handlers.wsgi import WSGIRequest

from .wsgi_util import wsgi


def handle_http_event(app):
    environ = wsgi(json.loads(sys.stdin.read()))
    app.load_middleware()
    resp = app.get_response(WSGIRequest(environ))

    body = ''
    if resp.streaming:
        for content in resp.streaming_content:
            body += content
    else:
        body = resp.content.decode('utf-8')

    headers = {}
    for header in resp.items():
        headers[header[0]] = header[1]
    resp.close()

    sys.stdout.write(json.dumps({
        'body': body,
        'status_code': resp.status_code,
        'headers': headers,
    }))
