""" Import the required modules """
from typing import Annotated, Self

from datetime import date
from pydantic import (
    ConfigDict,
    Field,
    computed_field
)

from modules.core.models.organization import OrganizationMinor
from modules.core.models.lookup import LookupMinor
from .user import User, UserDetail

# Import the enums
from modules.core.enums import Language

class UserFullResponse(User):
    """
    User model for the application.
    """
    avatar: str|None = Field(default=None, description="Avatar URL",
        exclude=False, max_length=4000
    )
    date_of_birth: date|None = Field(default=None, description="Date of Birth",
            exclude=False
        )
    gender_id: int = Field(default=0, description="Gender ID",
            exclude=True
        )
    language_id: int = Field(default=0, description="Language ID",
            exclude=True
        )
    is_pool: bool = Field(default=False, description="Is Pool User",
            exclude=False
        )
    is_active: bool = Field(default=True, description="Is Active",
            exclude=False
        )

    # Foreign Key to References
    organization: OrganizationMinor = Field(
            description="Organization",
            exclude=False
        )
    type: LookupMinor = Field(
            description="User Type",
            exclude=False
        )
    gender: LookupMinor = Field(
            description="Gender",
            exclude=False
        )
    # details: list[UserDetail] = Field(
    #         description="User Details",
    #         exclude=False
    #     )
