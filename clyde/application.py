from typing import Optional, Union

from aiohttp.web import HostSequence

from .http import HTTPClient, HTTPServer
from .models.snowflake import Snowflake, SnowflakeLike


class Application(object):
    def __init__(
        self,
        id: SnowflakeLike,
        public_key: Union[str, bytes],
        *,
        host: Optional[Union[str, HostSequence]] = None,
        port: Optional[int] = None,
    ) -> None:
        if isinstance(public_key, str):
            public_key = bytes.fromhex(public_key)

        self.id = Snowflake(id)

        self._client = HTTPClient(self.id)
        self._server = HTTPServer(
            host=host,
            port=port,
            public_key=public_key,
        )

    def run(self) -> None:
        self._server.run()
