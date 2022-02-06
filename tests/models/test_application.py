from nacl.signing import VerifyKey

from clyde.models.application import Application
from clyde.models.snowflake import Snowflake
from clyde.models.team import MembershipState, Team
from clyde.models.users import User, UserFlags


def test_application(shared_datadir):
    a = Application.parse_file(shared_datadir / 'application.json')

    # Application
    assert a.bot_public
    assert not a.bot_require_code_grant
    assert a.cover_image == '31deabb7e45b6c8ecfef77d2f99c81a5'
    assert a.description == 'Test'
    assert a.guild_id == Snowflake(290926798626357260)
    assert a.icon is None
    assert a.id == Snowflake(172150183260323840)
    assert a.name == 'Baba O-Riley'
    assert a.primary_sku_id == Snowflake(172150183260323840)
    assert a.slug == 'test'
    assert a.summary == 'This is a game'
    assert a.verify_key == VerifyKey(
        b'\x1e\x0a\x35\x60\x58\xd6\x27\xca\x38\xa5\xc8\xc9\x64\x88\x18\x06' +
        b'\x1d\x49\xe4\x9b\xd9\xda\x9e\x3a\xb1\x7d\x98\xad\x4d\x6b\x02\x08'
    )

    # Application.owner
    assert isinstance(a.owner, User)
    assert a.owner.avatar is None
    assert a.owner.discriminator == '1738'
    assert a.owner.flags is UserFlags.TEAM_PSEUDO_USER
    assert a.owner.username == 'i own a bot'

    # Application.team
    assert isinstance(a.team, Team)
    assert a.team.icon == 'dd9b7dcfdf5351b9c3de0fe167bacbe1'
    assert a.team.name == 'Example Team'

    # Application.team.members
    m = a.team.members[0]
    assert m.membership_state is MembershipState.ACCEPTED
    assert m.permissions == ['*']
    assert m.user.avatar == 'd9e261cd35999608eb7e3de1fae3688b'
    assert m.user.discriminator == '0001'
    assert m.user.username == 'Mr Owner'

    # Cross-comparisons
    assert a.team.id == m.team_id == Snowflake(531992624043786253)
    assert a.team.owner_user_id == m.user.id == Snowflake(511972282709709995)
