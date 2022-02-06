from enum import IntEnum
from typing import List, Literal, Optional

from pydantic import BaseModel, validator

from .snowflake import Snowflake
from .users import User


class MembershipState(IntEnum):
    INVITED = 1
    ACCEPTED = 2


class TeamMember(BaseModel):
    membership_state: MembershipState
    """ The user's membership state on the team. """

    permissions: List[Literal['*']]
    """ Will always be ``['*']``. """

    team_id: Snowflake
    """	The ID of the parent team of which they are a member. """

    user: User
    """ The avatar, discriminator, ID, and username of the user. """

    @validator('permissions')
    def __validate_permissions(cls, v):  # noqa: N805
        assert v == ['*']
        return v


class Team(BaseModel):
    """ A group of developers on Discord who want to collaborate on apps. """

    icon: Optional[str]
    """ A hash of the image of the team's icon. """

    id: Snowflake
    """ The unique ID of the team. """

    members: List[TeamMember]
    """ The members of the team. """

    name: str
    """ The name of the team. """

    owner_user_id: Snowflake
    """ The user ID of the current team owner. """
