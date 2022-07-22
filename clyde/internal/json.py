import functools

try:
    from orjson import dumps, loads
except ImportError:
    from json import dumps as __json_dumps
    from json import loads

    @functools.wraps(__json_dumps)
    def dumps(*args, **kwargs):
        return __json_dumps(*args, **kwargs).encode('utf-8')

__all__ = ['dumps', 'loads']
