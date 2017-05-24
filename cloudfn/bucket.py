import sys
import json


def handle_bucket_event(handle_fn):
    sys.stdout.write(handle_fn(json.loads(sys.stdin.read())))
