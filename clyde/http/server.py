import functools
import json
import logging
from json import JSONEncoder
from typing import Any, Optional, Union

from aiohttp import web
from aiohttp.web import HostSequence, Request, Response
from aiohttp.web_exceptions import HTTPBadRequest
from nacl.signing import VerifyKey
from pydantic import BaseModel

from ..interaction_handler import InteractionHandler
from ..models.interactions import Interaction, InteractionType
from .middleware import validate_signature

logger = logging.getLogger(__name__)


class HTTPServer:
    def __init__(
        self,
        *,
        host: Optional[Union[str, HostSequence]] = None,
        port: Optional[int] = None,
        path: str = '/',
        public_key: bytes,
    ) -> None:
        self.host = host
        self.port = port
        self.handler = InteractionHandler()

        self._app = web.Application(middlewares=[
            validate_signature(VerifyKey(public_key)),
        ])
        self._app.router.add_post(path, self._handle_interaction)

    def run(self) -> None:
        web.run_app(
            self._app,
            host=self.host,
            port=self.port,
            print=None,  # type: ignore[arg-type]
        )

    async def start(self):
        runner = web.AppRunner(self._app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        await runner.cleanup()

    async def stop(self):
        await self._app.shutdown()

    async def _handle_interaction(self, request: Request) -> Response:
        # Parse the interaction from JSON
        try:
            obj = await request.json()
            logger.debug('Received interaction: %r', await request.text())
            interaction = Interaction.parse_obj(obj)
        except Exception as e:
            logger.error('Failed to read interaction body')
            raise HTTPBadRequest(text='Invalid request') from e

        # Delegate it to the proper handler coroutine
        if interaction.type == InteractionType.PING:
            data = await self.handler.handle_ping(interaction)
        elif interaction.type == InteractionType.APPLICATION_COMMAND:
            data = await self.handler.handle_application_command(interaction)
        elif interaction.type == InteractionType.MESSAGE_COMPONENT:
            data = await self.handler.handle_message_component(interaction)
        else:
            raise HTTPBadRequest(text='Unknown interaction type')

        return web.json_response(data, dumps=_dumps_custom)


class PydanticJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, BaseModel):
            return o.dict(exclude_unset=True)

        return super().default(o)


_dumps_custom = functools.partial(
    json.dumps,
    cls=PydanticJSONEncoder,
    separators=(',', ':'),
    indent=None,
)
