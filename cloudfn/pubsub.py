import sys
import json


def handle_pubsub_event(handle_fn):
    return sys.stdout.write(handle_fn(json.loads(sys.stdin.read())))
