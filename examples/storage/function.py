from cloudfn.storage import handle_bucket_event


def bucket_handler(obj):
    print jsonpickle.encode(obj)


handle_bucket_event(bucket_handler)
