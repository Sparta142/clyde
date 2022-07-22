import sys
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .interactions import ApplicationCommandType
from .permissions import Permissions
from .snowflake import Snowflake

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

ApplicationCommandOption = Any  # TODO

_NameStr = Annotated[str, Field(min_length=1, max_length=32)]
_DescriptionStr = Annotated[str, Field(max_length=100)]
_OptionList = Annotated[List[ApplicationCommandOption], Field(max_items=25)]


# https://discord.com/developers/docs/interactions/application-commands#application-command-object
class ApplicationCommand(BaseModel):
    id: Snowflake
    """ Unique ID of command """

    type: Optional[ApplicationCommandType]
    """ Type of command, defaults to ``1`` """

    application_id: Snowflake
    """ ID of the parent application """

    guild_id: Optional[Snowflake]
    """ guild id of the command, if not global """

    name: _NameStr
    """ Name of command, 1-32 characters """

    name_localizations: Optional[Dict[str, _NameStr]]
    """
    Localization dictionary for ``name`` field.
    Values follow the same restrictions as ``name``
    """

    description: _DescriptionStr
    """
    Description for ``CHAT_INPUT`` commands, 1-100 characters.
    Empty string for ``USER`` and ``MESSAGE`` commands
    """

    description_localizations: Optional[Dict[str, _DescriptionStr]]
    """
    Localization dictionary for ``description`` field.
    Values follow the same restrictions as ``description``
    """

    options: Optional[_OptionList]
    """ Parameters for the command, max of 25 """

    default_member_permissions: Optional[Permissions]
    """ Set of permissions represented as a bit set """

    dm_permission: Optional[bool]
    """
    Indicates whether the command is available in DMs
    with the app, only for globally-scoped commands.
    By default, commands are visible.
    """

    default_permission: Optional[bool]
    """
    Not recommended for use as field will soon be deprecated.
    Indicates whether the command is enabled by default when
    the app is added to a guild, defaults to ``true``
    """

    version: Snowflake
    """
    Autoincrementing version identifier updated during
    substantial record changes
    """

# https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
# class ApplicationCommandOption(BaseModel):  # TODO
#     type
