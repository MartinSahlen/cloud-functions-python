from cloudfn.pubsub import handle_pubsub_event
import jsonpickle


def pubsub_handler(message):
    print jsonpickle.encode(message)


handle_pubsub_event(pubsub_handler)
