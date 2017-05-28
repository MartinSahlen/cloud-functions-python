import sys
import json
from wsgi_util import wsgi
from django.core.handlers.wsgi import WSGIRequest


def handle_http_event(app):
    environ = wsgi(json.loads(sys.stdin.read()))
    app.load_middleware()
    res = app.get_response(WSGIRequest(environ))
    
