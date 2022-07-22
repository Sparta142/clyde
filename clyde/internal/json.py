from typing import Any

_ENCODING = 'utf-8'

try:
    import orjson
    from orjson import loads

    def dumps_str(obj: Any) -> str:
        return orjson.dumps(obj).decode(_ENCODING)

    def dumps_bytes(obj: Any) -> bytes:
        return orjson.dumps(obj)
except ImportError:
    import json
    from json import loads

    def dumps_str(obj: Any) -> str:
        return json.dumps(obj)

    def dumps_bytes(obj: Any) -> bytes:
        return json.dumps(obj).encode(_ENCODING)


__all__ = ['dumps_bytes', 'dumps_str', 'loads']
