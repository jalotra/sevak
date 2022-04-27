

import json
import base64
from collections import OrderedDict

class SerialiseDeserialise:
    def serialise_jpg_bytes(self, jpg_bytes, md5hash = None, meta = {}):
        return self.serialise(OrderedDict(
            "meta" : meta
            "md5sum" : md5hash if md5hash is not None else self.get_hash(jpg_bytes)
            "bytes" : self.stringify_jpg(jpg_bytes)
        ))

    def get_hash(self, bytes):
        content_b64 = base64.b64encode(bytes)
        return hashlib.md5(content_b64).hexdigest()        

    def serialise(self, obj):
        return json.dumps(obj)
    
    def deserialise(self, obj):
        return json.loads(obj)
    
    def stringify_jpg(jpg_bytes):
        return base64.b64encode(jpg_bytes).decode('utf-8')

    def destringify_jpg(stringified_jpg):
        return base64.b64decode(stringified_jpg.encode('utf-8'))

