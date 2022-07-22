from typing import Any

from aiohttp.payload import BytesPayload

from clyde.internal.json import dumps


class JsonPayload(BytesPayload):
    def __init__(
        self,
        value: Any,
        content_type: str = 'application/json',
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            dumps(value),
            content_type=content_type,
            encoding='utf-8',
            *args,
            **kwargs,
        )
