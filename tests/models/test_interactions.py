from clyde.models.interactions import (ApplicationCommandInteractionData,
                                       Interaction, InteractionType)
from clyde.models.snowflake import Snowflake
from clyde.models.users import UserFlags


def test_ping_interaction_parse_raw():
    i = Interaction.parse_raw(b'{"application_id":"881397058114826261","id":"938242591147827220","token":"aW50ZXJhY3Rpb246OTM4MjQyNTkxMTQ3ODI3MjIwOmxqNU4wcXJOWnMwV2ZJMzhQMTRNRHhHdDZybnBiaTg5NGFGMDNXTkNhejhWNEFJQTlPdGtDUGV2TDZMQ0M0Y1ZYSEthaG1WM1RQdUdVYVU4TlJKNWczQjZ1ejEyd1lSTGF6b2l5czU2cG9hcmJUam9GTmJzYWlsQVBaUldyeW1n","type":1,"user":{"avatar":"da25f18552f9a643f28e4bb0985ea31e","discriminator":"3161","id":"211377592895406081","public_flags":256,"username":"House"},"version":1}')  # noqa: E501

    assert i.application_id == Snowflake(881397058114826261)
    assert i.channel_id is None
    assert i.data is None
    assert i.guild_id is None
    assert i.id == Snowflake(938242591147827220)
    assert i.member is None
    assert i.message is None
    assert i.token == 'aW50ZXJhY3Rpb246OTM4MjQyNTkxMTQ3ODI3MjIwOmxqNU4wcXJOWnMwV2ZJMzhQMTRNRHhHdDZybnBiaTg5NGFGMDNXTkNhejhWNEFJQTlPdGtDUGV2TDZMQ0M0Y1ZYSEthaG1WM1RQdUdVYVU4TlJKNWczQjZ1ejEyd1lSTGF6b2l5czU2cG9hcmJUam9GTmJzYWlsQVBaUldyeW1n'  # noqa: E501
    assert i.type is InteractionType.PING
    assert i.version == 1

    assert i.user.avatar == 'da25f18552f9a643f28e4bb0985ea31e'
    assert i.user.discriminator == '3161'
    assert i.user.id == Snowflake(211377592895406081)
    assert i.user.username == 'House'


def test_command_interaction_parse_raw():
    i = Interaction.parse_raw(b'{"application_id":"881397058114826261","channel_id":"704190879698649159","data":{"id":"881421400454344716","name":"blep","options":[{"name":"animal","type":3,"value":"animal_cat"}],"type":1},"guild_id":"376279481003802627","guild_locale":"en-US","id":"938315259217850398","locale":"en-US","member":{"avatar":null,"communication_disabled_until":null,"deaf":false,"is_pending":false,"joined_at":"2017-11-04T08:00:19.276000+00:00","mute":false,"nick":null,"pending":false,"permissions":"2199023255551","premium_since":null,"roles":["387325199227420672","379097058990096386"],"user":{"avatar":"da25f18552f9a643f28e4bb0985ea31e","discriminator":"3161","id":"211377592895406081","public_flags":256,"username":"House"}},"token":"aW50ZXJhY3Rpb246OTM4MzE1MjU5MjE3ODUwMzk4OkdFaE1qWkFpMDV3REZTWVJ2d0pKWUJRTHNVYUNaSDhTcm11d045dHoxc2tyZVZUcUU3Q2RNZzdOanR0RHR1dHhiNlB3bzVpUXpERDBqNWlVT1hrc296ampyVFRyMmk5b1pBVDRhRjc3THJNSlhNVVV2UkpZT1NickpkWXp5YmFO","type":2,"version":1}')  # noqa: E501

    assert i.application_id == Snowflake(881397058114826261)
    assert i.channel_id == Snowflake(704190879698649159)
    assert i.guild_id == Snowflake(376279481003802627)
    assert i.id == Snowflake(938315259217850398)
    assert i.token == 'aW50ZXJhY3Rpb246OTM4MzE1MjU5MjE3ODUwMzk4OkdFaE1qWkFpMDV3REZTWVJ2d0pKWUJRTHNVYUNaSDhTcm11d045dHoxc2tyZVZUcUU3Q2RNZzdOanR0RHR1dHhiNlB3bzVpUXpERDBqNWlVT1hrc296ampyVFRyMmk5b1pBVDRhRjc3THJNSlhNVVV2UkpZT1NickpkWXp5YmFO'  # noqa: E501
    assert i.type == InteractionType.APPLICATION_COMMAND
    assert i.version == 1

    assert isinstance(i.data, ApplicationCommandInteractionData)
    assert i.data.id == Snowflake(881421400454344716)
    assert i.data.name == 'blep'
    assert i.data.type == ApplicationCommandInteractionData.Type.CHAT_INPUT

    assert i.member.avatar is None
    assert not i.member.deaf
    assert not i.member.pending
    assert i.member.permissions == '2199023255551'  # TODO: Permissions object
    assert i.member.premium_since is None
    assert set(i.member.roles) == {  # Don't care about the order?
        Snowflake(387325199227420672),
        Snowflake(379097058990096386),
    }

    assert i.member.user.avatar == 'da25f18552f9a643f28e4bb0985ea31e'
    assert i.member.user.discriminator == '3161'
    assert i.member.user.id == Snowflake(211377592895406081)
    assert i.member.user.public_flags == UserFlags(256)
    assert i.member.user.username == 'House'
