from datetime import datetime
from enum import IntEnum, IntFlag
from typing import List, Optional

from pydantic import BaseModel, validator
from pydantic.color import Color

from .permissions import Permissions
from .snowflake import Snowflake


# https://discord.com/developers/docs/resources/user#user-object-premium-types
class PremiumType(IntEnum):
    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2


# https://discord.com/developers/docs/resources/user#user-object-user-flags
class UserFlags(IntFlag):
    NONE = 0
    STAFF = 1 << 0
    PARTNER = 1 << 1
    HYPESQUAD = 1 << 2
    BUG_HUNTER_LEVEL_1 = 1 << 3
    HYPESQUAD_ONLINE_HOUSE_1 = 1 << 6
    HYPESQUAD_ONLINE_HOUSE_2 = 1 << 7
    HYPESQUAD_ONLINE_HOUSE_3 = 1 << 8
    PREMIUM_EARLY_SUPPORTER = 1 << 9
    TEAM_PSEUDO_USER = 1 << 10
    BUG_HUNTER_LEVEL_2 = 1 << 14
    VERIFIED_BOT = 1 << 16
    VERIFIED_DEVELOPER = 1 << 17
    CERTIFIED_MODERATOR = 1 << 18
    BOT_HTTP_INTERACTIONS = 1 << 19


# https://discord.com/developers/docs/resources/user#user-object-user-structure
class User(BaseModel):
    id: Snowflake
    """
    The user's ID.

    Required OAuth2 scope: ``identify``
    """

    username: str
    """
    The user's username, not unique across the platform.

    Required OAuth2 scope: ``identify``
    """

    discriminator: str
    """
    The user's 4-digit discord-tag.

    Required OAuth2 scope: ``identify``
    """

    avatar: Optional[str]
    """
    The user's avatar hash.

    Required OAuth2 scope: ``identify``
    """

    bot: Optional[bool]
    """
    Whether the user belongs to an OAuth2 application. """

    system: Optional[bool]
    """
    Whether the user is an Official Discord System user
    (part of the urgent message system).


    Required OAuth2 scope: ``identify``
    """

    mfa_enabled: Optional[bool]
    """
    Whether the user has two factor enabled on their account.

    Required OAuth2 scope: ``identify``
    """

    banner: Optional[str]
    """
    The user's banner hash.

    Required OAuth2 scope: ``identify``
    """

    accent_color: Optional[Color]
    """
    The user's banner color encoded as an integer
    representation of hexadecimal color code.


    Required OAuth2 scope: ``identify``
    """

    locale: Optional[str]
    """
    The user's chosen language option.

    Required OAuth2 scope: ``identify``
    """

    verified: Optional[bool]
    """
    Whether the email on this account has been verified.

    Required OAuth2 scope: ``email``
    """

    email: Optional[bool]
    """
    The user's email.

    Required OAuth2 scope: ``email``
    """

    flags: Optional[UserFlags]
    """
    The flags on a user's account.

    Required OAuth2 scope: ``identify``
    """

    premium_type: Optional[PremiumType]
    """
    The type of Nitro subscription on a user's account.

    Required OAuth2 scope: ``identify``
    """

    public_flags: Optional[UserFlags]
    """
    The public flags on a user's account.

    Required OAuth2 scope: ``identify``
    """

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        return f'{self.username}#{self.discriminator}'

    @property
    def avatar_url(self) -> Optional[str]:
        base_url = 'https://cdn.discordapp.com'

        if self.avatar is None:
            num = int(self.discriminator) % 5
            return f'{base_url}/embed/avatars/{num}.png'
        else:
            return f'{base_url}/avatars/{self.id}/{self.avatar}.png'


# https://discord.com/developers/docs/resources/guild#guild-member-object
class GuildMember(BaseModel):
    user: Optional[User]
    """ The user this guild member represents. """

    nick: Optional[str]
    """ This user's guild nickname. """

    avatar: Optional[str]
    """ The member's guild avatar hash. """

    roles: List[Snowflake]
    """ Array of role object IDs. """

    joined_at: datetime
    """ When the user joined the guild. """

    premium_since: Optional[datetime]
    """ When the user started boosting the guild. """

    deaf: bool
    """ Whether the user is deafened in voice channels. """

    mute: bool
    """ Whether the user is muted in voice channels. """

    pending: Optional[bool]
    """
    Whether the user has not yet passed the guild's
    Membership Screening requirements.
    """

    permissions: Optional[Permissions]
    """
    Total permissions of the member in the channel,
    including overwrites, returned when in the interaction object.
    """

    communication_disabled_until: Optional[datetime]
    """
    When the user's timeout will expire and the user
    will be able to communicate in the guild again,
    null or a time in the past if the user is not timed out.
    """

    def __str__(self) -> str:
        return str(self.user) or self.nick or super().__str__()

    @property
    def timed_out(self) -> bool:
        """ Whether the user is currently timed out. """
        if self.communication_disabled_until:
            return self.communication_disabled_until < datetime.now()

        return False

    @validator('user', allow_reuse=True, pre=True)
    def __validate_user(cls, value):  # noqa: N805
        if value == {}:
            return None  # Normalize empty dict to None

        return value
