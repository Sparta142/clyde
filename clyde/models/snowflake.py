from datetime import datetime, timezone
from typing import Union

# A Unix timestamp in milliseconds
DISCORD_EPOCH = 1420070400000

RawSnowflake = Union[str, int]
SnowflakeLike = Union['Snowflake', RawSnowflake]


class Snowflake(int):
    """
    Implements Twitter's Snowflake format for uniquely
    identifiable descriptors (IDs).

    Guaranteed to be unique across all of Discord,
    except in some unique scenarios in which child objects
    share their parent's ID.
    """

    def __new__(cls, value: SnowflakeLike) -> 'Snowflake':
        if isinstance(value, Snowflake):
            return value

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
        return (self >> 22) + DISCORD_EPOCH

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
