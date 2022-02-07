from enum import IntEnum
from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel

from .messages import Message, MessageFlags
from .snowflake import Snowflake
from .users import GuildMember, User

# TODO: Remove these, for testing only
AllowedMentions = object
Channel = object
Component = object
Embed = object
InteractionDataOption = dict
PartialChannel = Channel
PartialGuildMember = GuildMember
PartialMessage = Message
Role = dict
SelectOptionValue = dict


# https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-type
class InteractionType(IntEnum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4


# https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-types
class ApplicationCommandType(IntEnum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3


# https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-resolved-data-structure
class ResolvedData(BaseModel):
    users: Optional[Dict[Snowflake, User]]
    members: Optional[Dict[Snowflake, PartialGuildMember]]
    roles: Optional[Dict[Snowflake, Role]]
    channels: Optional[Dict[Snowflake, PartialChannel]]
    messages: Optional[Dict[Snowflake, PartialMessage]]


# https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-data-structure
class ApplicationCommandData(BaseModel):
    id: Snowflake
    name: str
    type: ApplicationCommandType
    resolved: Optional[ResolvedData]
    options: Optional[List[InteractionDataOption]]
    target_id: Optional[Snowflake]


# https://discord.com/developers/docs/interactions/message-components#component-object-component-types
class ComponentType(IntEnum):
    ACTION_ROW = 1
    """ A container for other components. """

    BUTTON = 2
    """ A button object. """

    SELECT_MENU = 3
    """ A select menu for picking from choices. """


# https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-data-structure
class ComponentData(BaseModel):
    custom_id: Optional[str]
    component_type: Optional[ComponentType]
    values: Optional[List[str]]


InteractionData = Union[ApplicationCommandData, ComponentData]


# https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-structure
class Interaction(BaseModel):
    id: Snowflake
    """ ID of the interaction. """

    application_id: Snowflake
    """ ID of the application this interaction is for. """

    type: InteractionType
    """ The type of interaction. """

    data: Optional[InteractionData]
    """ The command data payload. """

    guild_id: Optional[Snowflake]
    """ The guild it was sent from. """

    channel_id: Optional[Snowflake]
    """ The channel it was sent from. """

    member: Optional[GuildMember]
    """ Guild member data for the invoking user, including permissions. """

    user: Optional[User]
    """ User object for the invoking user, if invoked in a DM. """

    token: str
    """ A continuation token for responding to the interaction. """

    version: Literal[1]
    """ Read-only property, always ``1``. """

    message: Optional[Message]
    """ For components, the message they were attached to. """

    locale: Optional[str]
    """ The selected language of the invoking user. """

    guild_locale: Optional[str]
    """ The guild's preferred locale, if invoked in a guild. """

    @property
    def from_guild(self) -> bool:
        return self.guild_id is not None

    @property
    def from_dm(self) -> bool:
        return self.user is not None


class InteractionCallbackType(IntEnum):
    PONG = 1
    """ ACK a Ping. """

    CHANNEL_MESSAGE_WITH_SOURCE = 4
    """ Respond to an interaction with a message. """

    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    """
    ACK an interaction and edit a response later,
    the user sees a loading state.
    """

    DEFERRED_UPDATE_MESSAGE = 6
    """
    For components, ACK an interaction and edit the original
    message later; the user does not see a loading state.
    """

    UPDATE_MESSAGE = 7
    """ For components, edit the message the component was attached to. """

    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    """ Respond to an autocomplete interaction with suggested choices. """


class InteractionCallbackData(BaseModel):
    tts: Optional[bool]
    content: Optional[str]
    embeds: Optional[List[Embed]]
    allowed_mentions: Optional[AllowedMentions]
    flags: Optional[MessageFlags]
    components: Optional[Component]


class InteractionResponse(BaseModel):
    type: InteractionCallbackType
    """ The type of response. """

    data: Optional[InteractionCallbackData]
    """ An optional response message. """
