from datetime import datetime
from enum import Enum, IntFlag
from typing import List, Optional, Union

from pydantic import BaseModel

from .snowflake import Snowflake
from .users import GuildMember, User

# TODO: Remove these, for testing only
Role = object
ChannelMention = object
Attachment = object
Embed = object
Reaction = object
MessageActivity = object
Application = object
MessageReference = object
MessageInteraction = object
Channel = object
MessageComponent = object
StickerItem = object
Sticker = object


# https://discord.com/developers/docs/resources/channel#message-object-message-types
class MessageType(Enum):
    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    GUILD_MEMBER_JOIN = 7
    USER_PREMIUM_GUILD_SUBSCRIPTION = 8
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1 = 9
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2 = 10
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12
    GUILD_DISCOVERY_DISQUALIFIED = 14
    GUILD_DISCOVERY_REQUALIFIED = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    THREAD_CREATED = 18
    REPLY = 19
    CHAT_INPUT_COMMAND = 20
    THREAD_STARTER_MESSAGE = 21
    GUILD_INVITE_REMINDER = 22
    CONTEXT_MENU_COMMAND = 23


# https://discord.com/developers/docs/resources/channel#message-object-message-flags
class MessageFlags(IntFlag):
    CROSSPOSTED = 1 << 0
    """
    This message has been published to subscribed channels
    (via Channel Following).
    """

    IS_CROSSPOST = 1 << 1
    """
    This message originated from a message in another channel
    (via Channel Following).
    """

    SUPPRESS_EMBEDS = 1 << 2
    """ Do not include any embeds when serializing this message. """

    SOURCE_MESSAGE_DELETED = 1 << 3
    """
    The source message for this crosspost has been deleted
    (via Channel Following).
    """

    URGENT = 1 << 4
    """ This message came from the urgent message system. """

    HAS_THREAD = 1 << 5
    """
    This message has an associated thread, with the same id as the message.
    """

    EPHEMERAL = 1 << 6
    """
    This message is only visible to the user who invoked the Interaction.
    """

    LOADING = 1 << 7
    """
    This message is an Interaction Response and the bot is "thinking".
    """


# https://discord.com/developers/docs/resources/channel#message-object-message-structure
class Message(BaseModel):
    id: Snowflake
    channel_id: Snowflake
    guild_id: Optional[Snowflake]
    author: User
    member: Optional[GuildMember]
    content: str
    timestamp: datetime
    edited_timestamp: Optional[datetime]
    tts: bool
    mention_everyone: bool
    mentions: List[User]
    mention_roles: List[Role]
    mention_channels: Optional[List[ChannelMention]]
    attachments: List[Attachment]
    embeds: List[Embed]
    reactions: Optional[List[Reaction]]
    nonce: Optional[Union[int, str]]
    pinned: bool
    webhook_id: Optional[Snowflake]
    type: MessageType
    activity: Optional[MessageActivity]
    application: Optional[Application]
    application_id: Optional[Snowflake]
    message_reference: Optional[MessageReference]
    flags: Optional[MessageFlags]
    referenced_message: Optional['Message']
    interaction: Optional[MessageInteraction]
    thread: Optional[Channel]
    components: Optional[List[MessageComponent]]
    sticker_items: Optional[List[StickerItem]]
    stickers: Optional[List[Sticker]]


Message.update_forward_refs()
