import sys
import json


def handle_http_event(handle_fn):
    # Should create a request like object
    sys.stdout.write(handle_fn(json.loads(sys.stdin.read())))
