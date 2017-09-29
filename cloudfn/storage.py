import json
import sys

from dateutil.parser import parse


def _update_attributes(obj, d, keys, default=None):
    """Updates the attributes of `obj` with keys from `d` in camelCase. """
    for key in keys:
        parts = key.split('_')
        camel_case = parts[0] + ''.join(map(str.title, parts[1:]))
        setattr(obj, key, d.get(camel_case, default))


class ACL:
    __ATTRIBUTES = (
        'kind', 'id', 'self_link', 'bucket', 'object', 'generation', 'entity',
        'role', 'email', 'entity_id', 'domain', 'project_team', 'etag'
    )

    def __init__(self, raw_json):
        _update_attributes(self, raw_json, self.__ATTRIBUTES)


class Object:
    __ATTRIBUTES = (
        'kind', 'id', 'self_link', 'bucket', 'name', 'generation',
        'metageneration', 'content_type', 'time_created', 'updated',
        'time_deleted', 'storage_class', 'time_storage_class_updated', 'size',
        'md5_hash', 'media_link', 'content_encoding', 'content_disposition',
        'content_language', 'cache_control', 'metadata', 'owner', 'crc32c',
        'component_count', 'customer_encryption'
    )

    def __init__(self, raw_json):
        _update_attributes(self, raw_json, self.__ATTRIBUTES)

        if self.time_created is not None:
            self.time_created = parse(self.time_created)
        if self.updated is not None:
            self.updated = parse(self.updated)
        if self.time_deleted is not None:
            self.time_deleted = parse(self.time_deleted)
        if self.time_storage_class_updated is not None:
            self.time_storage_class_updated = \
                parse(self.time_storage_class_updated)

        self.acl = list(map(ACL, raw_json.get('acl') or []))


def handle_bucket_event(handle_fn):
    handle_fn(Object(json.loads(sys.stdin.read())))
