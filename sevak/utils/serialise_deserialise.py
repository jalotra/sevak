

import json
import base64
from collections import OrderedDict
import hashlib

class SerialiseDeserialise:
    @staticmethod
    def serialise_jpg(jpg_bytes, md5hash = None, meta = {}):
        return SerialiseDeserialise.serialise(OrderedDict({
            "meta" : meta,
            "md5sum" : md5hash if md5hash is not None else SerialiseDeserialise.get_hash(jpg_bytes),
            "bytes" : SerialiseDeserialise.stringify_jpg(jpg_bytes)
        }))

    @staticmethod
    def get_hash(bytes):
        content_b64 = base64.b64encode(bytes)
        return hashlib.md5(content_b64).hexdigest()        

    @staticmethod
    def serialise(obj):
        return json.dumps(obj)
    
    @staticmethod
    def deserialise(obj):
        return json.loads(obj)
    
    @staticmethod
    def stringify_jpg(jpg_bytes):
        return base64.b64encode(jpg_bytes).decode('utf-8')

    def destringify_jpg(stringified_jpg):
        return base64.b64decode(stringified_jpg.encode('utf-8'))

