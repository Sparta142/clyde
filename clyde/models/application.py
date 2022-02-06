from typing import List, Optional

from nacl.encoding import HexEncoder
from nacl.signing import VerifyKey
from pydantic import BaseModel, validator
from yarl import URL

from .snowflake import Snowflake
from .team import Team
from .users import User


class Application(BaseModel, arbitrary_types_allowed=True):
    id: Snowflake
    """ The id of the app. """

    name: str
    """ The name of the app. """

    icon: Optional[str]
    """ The icon hash of the app. """

    description: str
    """ The description of the app. """

    rpc_origins: Optional[List[str]]
    """ An array of RPC origin urls, if RPC is enabled. """

    bot_public: bool
    """
    When ``False``, only the app owner can join
    the app's bot to guilds.
    """

    bot_require_code_grant: bool
    """
    When ``True``, the app's bot will only join upon
    completion of the full OAuth2 code grant flow.
    """

    terms_of_service_url: Optional[URL]
    """ The URL of the app's terms of service. """

    privacy_policy_url: Optional[URL]
    """ The URL of the app's privacy policy. """

    owner: Optional[User]
    """
    Partial ``User`` object containing info on the
    owner of the application.
    """

    summary: str
    """
    If this application is a game sold on Discord, this field
    will be the summary field for the store page of its primary SKU.
    """

    verify_key: VerifyKey
    """
    The hex encoded key for verification in interactions
    and the GameSDK's GetTicket.
    """

    team: Optional[Team]
    """
    If the application belongs to a team,
    this will be a list of the members of that team.
    """

    guild_id: Optional[Snowflake]
    """
    If this application is a game sold on Discord,
    this field will be the guild to which it has been linked.
    """

    primary_sku_id: Optional[Snowflake]
    """
    If this application is a game sold on Discord,
    this field will be the id of the "Game SKU" that is created, if exists.
    """

    slug: Optional[str]
    """
    If this application is a game sold on Discord,
    this field will be the URL slug that links to the store page.
    """

    cover_image: Optional[str]
    """ The application's default rich presence invite cover image hash. """

    flags: Optional[int]
    """ The application's public flags. """

    @validator('verify_key', pre=True)
    def __decode_verify_key(cls, v: str) -> VerifyKey:  # noqa: N805
        return VerifyKey(v.encode('ascii'), encoder=HexEncoder)
