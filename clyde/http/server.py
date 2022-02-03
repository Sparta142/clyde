import logging
from typing import Awaitable, Callable, Optional, Union

from aiohttp import web
from aiohttp.web import HostSequence, Request, Response, middleware
from aiohttp.web_exceptions import (HTTPBadRequest, HTTPNotFound,
                                    HTTPUnauthorized)
from aiohttp.web_response import StreamResponse
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from ..models.interactions import Interaction, InteractionType

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

        self._verify_key = VerifyKey(public_key)

        self._app = web.Application(middlewares=[self._validate_signature])
        self._app.add_routes([web.post(path, self._handle_interaction)])

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
        try:
            obj = await request.json()
            print(await request.read())
            interaction = Interaction.parse_obj(obj)
        except Exception as e:
            logger.error('Failed to read interaction body')
            raise HTTPBadRequest(text='Invalid request') from e

        if interaction.type == InteractionType.PING:
            return await self._handle_ping(request, interaction)
        elif interaction.type == InteractionType.APPLICATION_COMMAND:
            return await self._handle_app_cmd(request, interaction)
        elif interaction.type == InteractionType.MESSAGE_COMPONENT:
            return await self._handle_msg_component(request, interaction)
        else:
            raise HTTPBadRequest(text='Unknown interaction type')

    async def _handle_ping(
        self,
        request: Request,
        interaction: Interaction,
    ) -> Response:
        return web.json_response({'type': InteractionType.PING})

    async def _handle_app_cmd(
        self,
        request: Request,
        interaction: Interaction,
    ) -> Response:
        raise HTTPNotFound(text='Not implemented')

    async def _handle_msg_component(
        self,
        request: Request,
        interaction: Interaction,
    ) -> Response:
        raise HTTPNotFound(text='Not implemented')

    @middleware
    async def _validate_signature(
        self,
        request: Request,
        handler: Callable[[Request], Awaitable[StreamResponse]],
    ) -> StreamResponse:
        try:
            signature = request.headers['X-Signature-Ed25519']
            timestamp = request.headers['X-Signature-Timestamp']
        except KeyError as e:
            raise HTTPUnauthorized(text='Missing signature') from e

        # The signed message is the decoded body prefixed with the timestamp
        body = await request.text()
        smessage = (timestamp + body).encode()

        try:
            self._verify_key.verify(smessage, bytes.fromhex(signature))
        except BadSignatureError as e:
            raise HTTPUnauthorized(text='Invalid signature') from e

        # Everything looks good, continue handling
        return await handler(request)
