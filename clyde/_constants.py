from aiohttp import __version__ as aiohttp_version

from . import __version__ as clyde_version

# https://discord.com/developers/docs/reference#api-reference-base-url
DISCORD_BASE_URL = 'https://discord.com'

# Discord requires the User-Agent format to follow these guidelines:
# https://discord.com/developers/docs/reference#user-agent
CLYDE_USER_AGENT = (
    f'DiscordBot (https://github.com/Sparta142/clyde, {clyde_version}) ' +
    f'using aiohttp/{aiohttp_version}'
)
