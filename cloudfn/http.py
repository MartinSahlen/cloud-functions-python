import sys


def handle_http_event(handle_fn):
    sys.stdout.write(handle_fn(sys.stdin.read()))
