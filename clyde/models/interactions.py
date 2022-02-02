from enum import IntEnum, IntFlag
from typing import List, Mapping, Optional, Union

from pydantic import BaseModel

from .snowflake import Snowflake
from .users import GuildMember, User

# TODO: Remove these, for testing only
Role = object
Channel = object
Message = dict
Embed = object
AllowedMentions = object
Component = object


# https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-type
class InteractionType(IntEnum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4


class ResolvedData(BaseModel):
    users: Optional[Mapping[Snowflake, User]]
    members: Optional[Mapping[Snowflake, GuildMember]]
    roles: Optional[Mapping[Snowflake, Role]]
    channels: Optional[Mapping[Snowflake, Channel]]
    messages: Optional[Mapping[Snowflake, Message]]


class ApplicationCommandInteractionData(BaseModel):
    class Type(IntEnum):
        CHAT_INPUT = 1
        """
        Slash commands; a text-based command that shows up
        when a user types ``/``.
        """

        USER = 2
        """
        A UI-based command that shows up when you
        right click or tap on a user.
        """

        MESSAGE = 3
        """
        A UI-based command that shows up when you
        right click or tap on a message.
        """

    class Option(BaseModel):
        class Type(IntEnum):
            SUB_COMMAND = 1
            SUB_COMMAND_GROUP = 2
            STRING = 3
            INTEGER = 4  # Any integer between -2^53 and 2^53
            BOOLEAN = 5
            USER = 6
            CHANNEL = 7  # Includes all channel types + categories
            ROLE = 8
            MENTIONABLE = 9  # Includes users and roles
            NUMBER = 10  # Any double between -2^53 and 2^53

        name: str
        type: Type
        value: Optional[object]  # TODO
        options: Optional[List[object]]  # TODO

    id: Snowflake
    name: str
    type: Type
    resolved: Optional[ResolvedData]
    options: Optional[List[Option]]
    target_id: Optional[Snowflake]


class ComponentInteractionData(BaseModel):
    class Type(IntEnum):
        ACTION_ROW = 1
        BUTTON = 2
        SELECT_MENU = 3

    custom_id: str
    component_type: Type
    values: Optional[List[object]]


# https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-structure
class Interaction(BaseModel):
    id: Snowflake
    """ ID of the interaction. """

    application_id: Snowflake
    """ ID of the application this interaction is for. """

    type: InteractionType
    """ The type of interaction. """

    data: Optional[Union[
        ApplicationCommandInteractionData,
        ComponentInteractionData,
    ]]
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

    version: int
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


class InteractionCallbackDataFlags(IntFlag):
    EPHEMERAL = 1 << 6
    """ Only the user receiving the message can see it. """


class InteractionCallbackData(BaseModel):
    tts: Optional[bool]
    content: Optional[str]
    embeds: Optional[List[Embed]]
    allowed_mentions: Optional[AllowedMentions]
    flags: Optional[InteractionCallbackDataFlags]
    components: Optional[Component]


class InteractionResponse(BaseModel):
    type: InteractionCallbackType
    """ The type of response. """

    data: Optional[InteractionCallbackData]
    """ An optional response message. """
