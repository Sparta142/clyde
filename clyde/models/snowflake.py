from datetime import datetime, timezone
from typing import Union


class Snowflake(int):
    def __new__(cls, value: Union[int, str]) -> 'Snowflake':
        if not isinstance(value, (int, str)):
            raise TypeError(
                f'Expected value to be int or str, but it was {type(value)}')

        if not (0 <= int(value) < 2**64):
            raise ValueError(f'Value out of bounds: {value}')

        return super().__new__(cls, value)

    def __repr__(self) -> str:
        return f'Snowflake({int(self)})'

    def __str__(self) -> str:
        return str(int(self))

    @property
    def timestamp(self) -> int:
        return (self >> 22) + 1420070400000

    @property
    def time(self) -> datetime:
        return datetime.fromtimestamp(self.timestamp / 1000.0, tz=timezone.utc)

    @property
    def worker_id(self) -> int:
        return (self & 0x3e0000) >> 17

    @property
    def process_id(self) -> int:
        return (self & 0x1f000) >> 22

    @property
    def sequence(self) -> int:
        return self & 0xfff
