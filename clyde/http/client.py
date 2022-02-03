import aiohttp

from .. import __version__
from ..models.snowflake import Snowflake

# https://discord.com/developers/docs/reference#api-reference-base-url
DISCORD_BASE_URL = 'https://discord.com/api/v9'

# Discord requires the User-Agent format to follow these guidelines:
# https://discord.com/developers/docs/reference#user-agent
USER_AGENT = (
    f'DiscordBot (https://github.com/Sparta142/clyde, {__version__}) '
    f'using aiohttp/{aiohttp.__version__}'
)


class HTTPClient:
    def __init__(self, application_id: Snowflake) -> None:
        self.application_id = application_id
        self.base_url = f'{DISCORD_BASE_URL}/applications/{application_id!s}'

        # Initialized in __aenter__
        self._session: aiohttp.ClientSession

    async def __aenter__(self) -> 'HTTPClient':
        self._session = aiohttp.ClientSession(headers={
            aiohttp.hdrs.USER_AGENT: USER_AGENT,
        })
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        await self._session.close()
