import sys
from io import BytesIO

import six
from six.moves.urllib_parse import urlparse


def wsgi(raw_json):
    components = urlparse(raw_json['url'])
    path = components.path
    if path == '':
        path = '/'
    port = components.port
    if port is None:
        # We'll just leet it go
        port = 1337

    buf = bytearray(raw_json.get('body', u''), 'utf-8')

    environ = {
        'PATH_INFO': path,
        'QUERY_STRING': components.query,
        'REQUEST_METHOD': raw_json['method'],
        'SERVER_NAME': components.hostname,
        'SERVER_PORT': port,
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'SERVER_SOFTWARE': 'CloudFunctions/1.0',
        'CONTENT_LENGTH': len(buf),
        'wsgi.errors': sys.stderr,
        'wsgi.input': BytesIO(buf),
        'wsgi.multiprocess': False,
        'wsgi.multithread': False,
        'wsgi.run_once': False,
        'wsgi.url_scheme': components.scheme,
        'wsgi.version': (1, 0),
    }
    headers = raw_json.get('headers', None)
    if headers is not None:
        for key, value in six.iteritems(headers):
            environ['HTTP_' + key.replace('-', '_').upper()] = value
    return environ
