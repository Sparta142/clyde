from enum import EnumMeta, IntFlag


class _StringyEnumMeta(EnumMeta):
    """
    Converts the ``value`` parameter of ``__call__``
    to an int (if it's a str) before attempting to
    do the value lookup.

    This is to make Discord API interop more convenient for
    integer enums that are passed around as strings and not ints.
    """

    def __call__(cls, value, names=None, **kwargs):  # noqa: N805
        if names is None and isinstance(value, str):
            value = int(value)

        return super().__call__(value, names, **kwargs)


# https://discord.com/developers/docs/topics/permissions
class Permissions(IntFlag, metaclass=_StringyEnumMeta):
    """
    Permissions in Discord are a way to limit and grant
    certain abilities to users.

    A set of base permissions can be configured at the guild level
    for different roles. When these roles are attached to users,
    they grant or revoke specific privileges within the guild.

    Along with the guild-level permissions, Discord also supports
    permission overwrites that can be assigned to individual guild
    roles or guild members on a per-channel basis.
    """

    CREATE_INSTANT_INVITE = 1 << 0
    """ Allows creation of instant invites. """

    KICK_MEMBERS = 1 << 1
    """ Allows kicking members. """

    BAN_MEMBERS = 1 << 2
    """ Allows banning members. """

    ADMINISTRATOR = 1 << 3
    """ Allows all permissions and bypasses channel permission overwrites. """

    MANAGE_CHANNELS = 1 << 4
    """ Allows management and editing of channels. """

    MANAGE_GUILD = 1 << 5
    """ Allows management and editing of the guild. """

    ADD_REACTIONS = 1 << 6
    """ Allows for the addition of reactions to messages. """

    VIEW_AUDIT_LOG = 1 << 7
    """ Allows for viewing of audit logs. """

    PRIORITY_SPEAKER = 1 << 8
    """ Allows for using priority speaker in a voice channel. """

    STREAM = 1 << 9
    """ Allows the user to go live. """

    VIEW_CHANNEL = 1 << 10
    """
    Allows guild members to view a channel,
    which includes reading messages in text channels.
    """

    SEND_MESSAGES = 1 << 11
    """
    Allows for sending messages in a channel
    (does not allow sending messages in threads).
    """

    SEND_TTS_MESSAGES = 1 << 12
    """ Allows for sending of ``/tts`` messages. """

    MANAGE_MESSAGES = 1 << 13
    """ Allows for deletion of other users messages. """

    EMBED_LINKS = 1 << 14
    """ Links sent by users with this permission will be auto-embedded. """

    ATTACH_FILES = 1 << 15
    """ Allows for uploading images and files. """

    READ_MESSAGE_HISTORY = 1 << 16
    """ Allows for reading of message history. """

    MENTION_EVERYONE = 1 << 17
    """
    Allows for using the ``@everyone`` tag to notify all
    users in a channel, and the ``@here`` tag to notify
    all online users in a channel.
    """

    USE_EXTERNAL_EMOJIS = 1 << 18
    """ Allows the usage of custom emojis from other servers. """

    VIEW_GUILD_INSIGHTS = 1 << 19
    """ Allows for viewing guild insights. """

    CONNECT = 1 << 20
    """ Allows for joining of a voice channel. """

    SPEAK = 1 << 21
    """ Allows for speaking in a voice channel. """

    MUTE_MEMBERS = 1 << 22
    """ Allows for muting members in a voice channel. """

    DEAFEN_MEMBERS = 1 << 23
    """ Allows for deafening of members in a voice channel. """

    MOVE_MEMBERS = 1 << 24
    """ Allows for moving of members between voice channels. """

    USE_VAD = 1 << 25
    """ Allows for using voice-activity-detection in a voice channel. """

    CHANGE_NICKNAME = 1 << 26
    """ Allows for modification of own nickname. """

    MANAGE_NICKNAMES = 1 << 27
    """ Allows for modification of other users nicknames. """

    MANAGE_ROLES = 1 << 28
    """ Allows management and editing of roles. """

    MANAGE_WEBHOOKS = 1 << 29
    """ Allows management and editing of webhooks. """

    MANAGE_EMOJIS_AND_STICKERS = 1 << 30
    """ Allows management and editing of emojis and stickers. """

    USE_APPLICATION_COMMANDS = 1 << 31
    """
    Allows members to use application commands,
    including slash commands and context menu commands.
    """

    REQUEST_TO_SPEAK = 1 << 32
    """
    Allows for requesting to speak in stage channels.

    (This permission is under active development
    and may be changed or removed.)
    """

    MANAGE_EVENTS = 1 << 33
    """ Allows for creating, editing, and deleting scheduled events. """

    MANAGE_THREADS = 1 << 34
    """
    Allows for deleting and archiving threads,
    and viewing all private threads.
    """

    CREATE_PUBLIC_THREADS = 1 << 35
    """ Allows for creating public and announcement threads. """

    CREATE_PRIVATE_THREADS = 1 << 36
    """ Allows for creating private threads. """

    USE_EXTERNAL_STICKERS = 1 << 37
    """ Allows the usage of custom stickers from other servers. """

    SEND_MESSAGES_IN_THREADS = 1 << 38
    """ Allows for sending messages in threads. """

    START_EMBEDDED_ACTIVITIES = 1 << 39
    """
    Allows for launching activities (applications with
    the ``EMBEDDED`` flag) in a voice channel.
    """

    MODERATE_MEMBERS = 1 << 40
    """
    Allows for timing out users to prevent them from
    sending or reacting to messages in chat and threads,
    and from speaking in voice and stage channels.
    """

    # Aliases for names used by the Discord client
    MANAGE_PERMISSIONS = MANAGE_ROLES
    USE_VOICE_ACTIVITY = USE_VAD
    TIMEOUT_MEMBERS = MODERATE_MEMBERS

    # TODO: Convenience functions and properties, a la discord.py
