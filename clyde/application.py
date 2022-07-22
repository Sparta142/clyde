import asyncio
import inspect
import logging
import sys
from typing import Callable, Dict, Iterable, List, Optional, TypeVar

import aiohttp
from aiohttp import web
from aiohttp.hdrs import AUTHORIZATION, USER_AGENT
from aiohttp.web_exceptions import HTTPBadRequest

from ._constants import CLYDE_USER_AGENT, DISCORD_BASE_URL
from .context import Context
from .http.middleware import validate_signature
from .http.payload import JsonPayload
from .internal.json import dumps_str, loads
from .models.application import Application
from .models.command import ApplicationCommand
from .models.interactions import (
    ApplicationCommandData,
    ApplicationCommandType,
    Interaction,
)
from .models.locale import Locale, LocaleLike
from .models.snowflake import Snowflake, SnowflakeLike

logger = logging.getLogger(__name__)

_TFunc = TypeVar('_TFunc', bound=Callable)
LocalizationDict = Dict[LocaleLike, str]


class ClydeApp:
    def __init__(self, token: str) -> None:
        self.token = token

        self._pending_registrations: List[dict] = []

        # Initialized by __aenter__
        self._session: aiohttp.ClientSession
        self._application: Application
        self._runner: web.AppRunner

    async def __aenter__(self) -> 'ClydeApp':
        self._session = aiohttp.ClientSession(
            base_url=DISCORD_BASE_URL,
            headers={
                AUTHORIZATION: 'Bot ' + self.token,
                USER_AGENT: CLYDE_USER_AGENT
            },
            raise_for_status=True,
            json_serialize=dumps_str,
        )
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._session is not None:
            await self._session.close()

        if self._runner is not None:
            await self._runner.cleanup()

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
        """
        Run the Discord application.

        :param host: The network host to listen on
        :type host: str, optional
        :param port: The TCP port to listen on
        :type port: int, optional
        """
        async def _main() -> None:
            async with self:
                await self._fetch_application_info()

                for reg in self._pending_registrations:
                    await self._register_command(reg)

                await self._run_web_server(host=host, port=port)
                await self._sleep_forever()

        return asyncio.run(_main())

    def chat_input(
        self,
        description: str,
        *,
        name: Optional[str] = None,
        name_localizations: Optional[LocalizationDict] = None,
        description_localizations: Optional[LocalizationDict] = None,
        guilds: Optional[Iterable[SnowflakeLike]] = None,
        dm_permission: Optional[bool] = None,
    ) -> Callable[[_TFunc], _TFunc]:
        if guilds is not None and dm_permission is not None:
            raise ValueError('Cannot specify both guilds and dm_permission')

        if not (1 <= len(description) <= 100):
            raise ValueError(
                'description must be between 1 and 100 characters')

        name_localizations = self._fixup_localizations(name_localizations, 32)
        description_localizations = \
            self._fixup_localizations(description_localizations, 100)

        # Normalize `guilds` to a tuple of Snowflakes
        if guilds is not None:
            guilds = tuple(Snowflake(value) for value in guilds)

        def decorator(func: Callable):  # TODO: Implement this
            nonlocal name

            # Use the function name if no command name is provided
            name = name or func.__name__

            if not (1 <= len(name) <= 32):
                raise ValueError('name must be between 1 and 32 characters')

            sig = inspect.signature(func)

            # Verify `ctx` parameter
            try:
                ctx_param = sig.parameters['ctx']
            except KeyError as e:
                raise TypeError(
                    f"{func.__name__} requires a 'ctx' parameter "
                    f'annotated as clyde.context.Context'
                ) from e

            if ctx_param.annotation != Context:
                raise TypeError(
                    f"{func.__name__} requires a 'ctx' parameter "
                    f'annotated as clyde.context.Context'
                )

            # Log the type of command we've determined `func` to be
            if guilds is not None:
                logging.debug('Registering guild command: %r', func)
            else:
                logging.debug('Registering global command: %r', func)

            # TODO: PLACEHOLDER
            self._pending_registrations.append({
                'name': name,
                'name_localizations': name_localizations or {},
                'description': description,
                'description_localizations': description_localizations or {},
                'options': [],
                # 'default_member_permissions': '',
                # 'dm_permission': dm_permission,
                'default_permission': True,
                'type': ApplicationCommandType.CHAT_INPUT,
            })

            return func

        return decorator

    async def _fetch_application_info(self) -> None:
        """
        Fetch this application's info from Discord and
        store it in `self._application`.
        """

        async with self._session.get(
            '/api/v9/oauth2/applications/@me',
        ) as response:
            self._application = Application.parse_obj(
                await response.json(loads=loads),
            )

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
        """
        Create an aiohttp web server to receive interactions with,
        then start it.

        :param host: The network host to listen on
        :type host: str, optional
        :param port: The TCP port to listen on
        :type port: int, optional
        """

        # Create aiohttp web application
        webapp = web.Application(
            middlewares=[validate_signature(self._application.verify_key)],
        )
        webapp.router.add_post('/', self._handle_post)

        self._runner = web.AppRunner(webapp)
        await self._runner.setup()

        site = web.TCPSite(self._runner, host=host, port=port)
        await site.start()

    async def _handle_post(self, request: web.Request) -> web.Response:
        # Parse the interaction from JSON
        try:
            interaction = Interaction.parse_obj(await request.json())
        except Exception as e:
            logger.error('Failed to read interaction body')
            raise HTTPBadRequest(text='Invalid request') from e
        else:
            logger.debug('Incoming interaction: %r', interaction)

            # TODO: Remove this
            if isinstance(interaction.data, ApplicationCommandData):
                logger.debug(
                    'Interaction options: %r', interaction.data.options)

        return web.json_response(None)  # TODO: Handle interaction

    async def _register_command(self, data: dict) -> None:
        async with self._session.post(
            f'/api/v9/applications/{self.application.id}/commands',
            data=JsonPayload(data),
        ) as response:
            jj = await response.json()
            _ = ApplicationCommand.parse_obj(jj)  # TODO

    @staticmethod
    def _fixup_localizations(
        data: Optional[LocalizationDict],
        max_length: int,
    ) -> Optional[LocalizationDict]:
        if data is None:
            return None

        new_data = {}

        for k, v in data.items():
            if not Locale.is_valid(k):
                raise ValueError(
                    f'Unknown locale: {k!r} (see '
                    'https://discord.com/developers/docs/reference#locales)'
                )

            if not isinstance(v, str):
                raise TypeError(
                    'Localization value must be str, not ' + type(v).__name__)

            if not (1 <= len(v) <= max_length):
                raise ValueError(
                    f'Localization for locale {k!r} must be '
                    f'between 1 and {max_length} characters'
                )

            if isinstance(k, Locale):
                new_data[k.value] = v
            elif isinstance(k, str):
                new_data[k] = v
            else:
                raise TypeError(
                    'Localization key must be str or Locale, not ' +
                    type(k).__name__
                )

        return new_data

    @staticmethod
    async def _sleep_forever():
        if sys.platform == 'win32' and sys.version_info < (3, 8):
            delay = 1
        else:
            delay = 3600

        while True:
            await asyncio.sleep(delay)
