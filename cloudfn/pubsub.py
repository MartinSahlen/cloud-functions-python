import json
import sys

from dateutil.parser import parse


class Message:
    def __init__(self, raw_json):
        self.data = raw_json.get('data', None),
        self.message_id = raw_json.get('messageId', None)
        self.attributes = raw_json.get('attributes', None),
        self.publish_time = raw_json.get('publishTime', None)
        if self.publish_time is not None:
            self.publish_time = parse(self.publish_time)


def handle_pubsub_event(handle_fn):
    handle_fn(Message(json.loads(sys.stdin.read())))
