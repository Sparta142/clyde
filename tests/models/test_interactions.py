from clyde.models.interactions import (
    ApplicationCommandData,
    ApplicationCommandType,
    Interaction,
    InteractionType,
)
from clyde.models.permissions import Permissions
from clyde.models.snowflake import Snowflake
from clyde.models.users import UserFlags


def test_message_command(shared_datadir):
    _ = Interaction.parse_file(shared_datadir / 'message_command.json')


def test_message_component(shared_datadir):
    _ = Interaction.parse_file(shared_datadir / 'message_component.json')


def test_select_menu_message_component(shared_datadir):
    _ = Interaction.parse_file(
        shared_datadir / 'select_menu_message_component.json')


def test_slash_command(shared_datadir):
    i = Interaction.parse_file(shared_datadir / 'slash_command.json')

    # Interaction
    assert i.application_id == Snowflake(881397058114826261)
    assert i.channel_id == Snowflake(704190879698649159)
    assert i.guild_id == Snowflake(376279481003802627)
    assert i.id == Snowflake(938980050605326376)
    assert i.token == 'EXAMPLE_TOKEN'
    assert i.type is InteractionType.APPLICATION_COMMAND
    assert i.version == 1

    # Interaction.data
    assert isinstance(i.data, ApplicationCommandData)
    assert i.data.id == Snowflake(881421400454344716)
    assert i.data.name == 'blep'
    assert i.data.type is ApplicationCommandType.CHAT_INPUT

    # Interaction.member
    assert i.member.avatar is None
    assert not i.member.deaf
    assert not i.member.pending
    assert i.member.permissions == Permissions(2199023255551)
    assert i.member.premium_since is None
    assert i.member.roles == [
        Snowflake(387325199227420672),
        Snowflake(379097058990096386),
    ]

    # Interaction.member.user
    assert i.member.user.avatar == 'da25f18552f9a643f28e4bb0985ea31e'
    assert i.member.user.discriminator == '3161'
    assert i.member.user.id == Snowflake(211377592895406081)
    assert i.member.user.public_flags is UserFlags.HYPESQUAD_ONLINE_HOUSE_3
    assert i.member.user.username == 'House'


def test_user_command(shared_datadir):
    _ = Interaction.parse_file(shared_datadir / 'user_command.json')


def test_ping_interaction(shared_datadir):
    i = Interaction.parse_file(shared_datadir / 'ping_interaction.json')

    # Interaction
    assert i.application_id == Snowflake(881397058114826261)
    assert i.channel_id is None
    assert i.data is None
    assert i.guild_id is None
    assert i.id == Snowflake(938979083671441448)
    assert i.member is None
    assert i.message is None
    assert i.token == 'A_TOKEN'
    assert i.type is InteractionType.PING
    assert i.version == 1

    # Interaction.user
    assert i.user.avatar == 'da25f18552f9a643f28e4bb0985ea31e'
    assert i.user.discriminator == '3161'
    assert i.user.id == Snowflake(211377592895406081)
    assert i.user.username == 'House'
