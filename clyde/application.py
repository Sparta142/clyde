import asyncio
import inspect
import logging
import sys
from typing import Optional

import aiohttp
from aiohttp import web
from aiohttp.hdrs import AUTHORIZATION, USER_AGENT
from aiohttp.web_exceptions import HTTPBadRequest

from . import __version__
from .http.middleware import validate_signature
from .models.application import Application
from .models.interactions import Interaction
from .models.snowflake import Snowflake

# https://discord.com/developers/docs/reference#api-reference-base-url
DISCORD_BASE_URL = 'https://discord.com'

# Discord requires the User-Agent format to follow these guidelines:
# https://discord.com/developers/docs/reference#user-agent
DISCORD_USER_AGENT = (
    f'DiscordBot (https://github.com/Sparta142/clyde, {__version__}) ' +
    f'using aiohttp/{aiohttp.__version__}'
)

logger = logging.getLogger(__name__)


class ClydeApp:
    def __init__(self, token: str) -> None:
        self.token = token

        # Initialized by __aenter__
        self._session: aiohttp.ClientSession
        self._application: Application
        self._webapp: web.Application

    async def __aenter__(self) -> 'ClydeApp':
        self._session = aiohttp.ClientSession(
            base_url=DISCORD_BASE_URL,
            headers={
                AUTHORIZATION: 'Bot ' + self.token,
                USER_AGENT: DISCORD_USER_AGENT
            },
            raise_for_status=True,
        )
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self._session.close()
        # TODO: Server

    @property
    def application(self) -> Application:
        return self._application

    @property
    def id(self) -> Snowflake:
        return self._application.id

    def run(
        self,
        *,
        host: Optional[str] = None,
        port: Optional[int] = None,
    ) -> None:
        async def _main():
            async with self:
                await self._fetch_application_info()
                await self._run_web_server(host=host, port=port)

        asyncio.run(_main())

    def chat_input(self, *dargs, **dkwargs):
        def decorator(func):
            print(inspect.signature(func, follow_wrapped=True))
            print(dargs, dkwargs)
            return func

        return decorator

    async def _fetch_application_info(self) -> None:
        # Fetch application info from Discord and cache it
        async with self._session.get(
            '/api/v9/oauth2/applications/@me',
        ) as response:
            self._application = Application.parse_obj(await response.json())

        # Log application developer page
        logger.info(
            'Started as https://discord.com/developers/applications/%s',
            self.application.id,
        )

    async def _run_web_server(
        self,
        *,
        host: Optional[str] = None,
        port: Optional[int] = None,
    ) -> None:
        # Create aiohttp web application
        self._webapp = web.Application(
            middlewares=[validate_signature(self._application.verify_key)],
        )
        self._webapp.router.add_post('/', self._handle_post)

        runner = web.AppRunner(self._webapp)
        await runner.setup()
        site = web.TCPSite(runner, host=host, port=port)
        await site.start()

        # Sleep forever
        if sys.platform == 'win32' and sys.version_info < (3, 8):
            delay = 1
        else:
            delay = 3600

        while True:
            await asyncio.sleep(delay)

    async def _handle_post(self, request: web.Request) -> web.Response:
        # Parse the interaction from JSON
        try:
            interaction = Interaction.parse_obj(await request.json())
        except Exception as e:
            logger.error('Failed to read interaction body')
            raise HTTPBadRequest(text='Invalid request') from e
        else:
            logger.debug('Incoming interaction: %r', interaction)

        return web.json_response(None)  # TODO
