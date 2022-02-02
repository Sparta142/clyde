from clyde.models.users import GuildMember


# https://discord.com/developers/docs/resources/guild#guild-member-object-example-guild-member
def test_example_guild_member():
    gm = GuildMember.parse_raw('''{
  "user": {},
  "nick": "NOT API SUPPORT",
  "avatar": null,
  "roles": [],
  "joined_at": "2015-04-26T06:26:56.936000+00:00",
  "deaf": false,
  "mute": false
}''')

    assert gm.avatar is None
    assert gm.communication_disabled_until is None
    assert gm.roles == []
    assert not gm.deaf
    assert not gm.mute
    assert not gm.timed_out
