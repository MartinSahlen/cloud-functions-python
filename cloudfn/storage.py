import sys
import json
from dateutil.parser import parse


class ACL:
    def __init__(self, raw_json):
        self.kind = raw_json.get('kind', None)
        self.id = raw_json.get('id', None)
        self.self_link = raw_json.get('selfLink', None)
        self.bucket = raw_json.get('bucket', None)
        self.object = raw_json.get('object', None)
        self.generation = raw_json.get('generation', None)
        self.entity = raw_json.get('entity', None)
        self.role = raw_json.get('role', None)
        self.email = raw_json.get('email', None)
        self.entity_id = raw_json.get('entityId', None)
        self.domain = raw_json.get('domain', None)
        self.project_team = raw_json.get('projectTeam', None)
        self.etag = raw_json.get('etag', None)


class Object:
    def __init__(self, raw_json):
        self.kind = raw_json.get('kind', None)
        self.id = raw_json.get('id', None)
        self.self_link = raw_json.get('selfLink', None)
        self.bucket = raw_json.get('bucket', None)
        self.generation = raw_json.get('generation', None)
        self.metageneration = raw_json.get('metageneration', None)
        self.content_type = raw_json.get('contentType', None)
        self.time_created = raw_json.get('timeCreated', None)
        self.updated = raw_json.get('updated', None)
        self.time_deleted = raw_json.get('timeDeleted', None)
        self.storage_class = raw_json.get('storageClass', None)
        self.time_storage_class_updated = \
            raw_json.get('timeStorageClassUpdated', None)
        self.size = raw_json.get('size', None)
        self.md5_hash = raw_json.get('md5_hash', None)
        self.media_link = raw_json.get('mediaLink', None)
        self.content_encoding = raw_json.get('contentEncoding', None)
        self.content_disposition = raw_json.get('contentDisposition', None)
        self.content_language = raw_json.get('contentLanguage', None)
        self.cache_control = raw_json.get('cacheControl', None)
        self.metadata = raw_json.get('metadata', None)
        self.owner = raw_json.get('owner', None)
        self.crc32c = raw_json.get('crc32c', None)
        self.component_count = raw_json.get('componentCount', None)
        self.customer_encryption = raw_json.get('customerEncryption', None)

        if self.time_created is not None:
            self.time_created = parse(self.time_created)
        if self.updated is not None:
            self.updated = parse(self.updated)
        if self.time_deleted is not None:
            self.time_deleted = parse(self.time_deleted)
        if self.time_storage_class_updated is not None:
            self.time_storage_class_updated = \
                parse(self.time_storage_class_updated)

        self.acl = []
        acl = raw_json.get('acl', None)

        if acl is not None:
            for a in acl:
                self.acl.append(ACL(a))


def handle_bucket_event(handle_fn):
    handle_fn(Object(json.loads(sys.stdin.read())))
