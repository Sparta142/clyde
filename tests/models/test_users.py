from clyde.models.users import GuildMember


# https://discord.com/developers/docs/resources/guild#guild-member-object-example-guild-member
def test_example_guild_member(shared_datadir):
    gm = GuildMember.parse_file(shared_datadir / 'guild_member.json')

    assert gm.avatar is None
    assert gm.communication_disabled_until is None
    assert gm.roles == []
    assert not gm.deaf
    assert not gm.mute
    assert not gm.timed_out

    assert str(gm) == 'NOT API SUPPORT'
