from urlparse import urlparse
import sys
from io import StringIO


def wsgi(raw_json):
    components = urlparse(raw_json['url'])
    path = components.path
    if path == '':
        path = '/'
    environ = {
        'PATH_INFO': path,
        'QUERY_STRING': components.query,
        'REQUEST_METHOD': raw_json['method'],
        'SERVER_NAME': components.hostname,
        'SERVER_PORT': components.port,
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'SERVER_SOFTWARE': 'CloudFunctions/1.0',
        'wsgi.errors': sys.stderr,
        'wsgi.input': StringIO(raw_json.get('body', u'')),
        'wsgi.multiprocess': False,
        'wsgi.multithread': False,
        'wsgi.run_once': False,
        'wsgi.url_scheme': components.scheme,
        'wsgi.version': (1, 0),
    }
    headers = raw_json.get('headers', None)
    if headers is not None:
        for key, value in headers.iteritems():
            environ['HTTP_' + key.replace('-', '_').upper()] = value
    return environ
