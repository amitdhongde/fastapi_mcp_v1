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
from modules.user.models import UserMinor
from .base import Auth

# Import the enums
from modules.core.enums import Language

class AuthFullResponse(Auth):
    """
    Auth model for the application.
    """
    id: int = Field(exclude=True)
    privileges: list = []
    settings: list = []
    unread_notifications: int = 0

    # Foreign Key to References
    organization: OrganizationMinor = Field(
            description="Organization",
            exclude=False
        )
    type: LookupMinor = Field(
            description="Auth Type",
            exclude=False
        )
    user: UserMinor = Field(
            description="User",
            exclude=False
        )

    model_config = ConfigDict(
        extra='allow',
        from_attributes=True
    )

class AuthMinorResponse(Auth):
    """
    Auth model for the application.
    """
    id: int = Field(exclude=True)
    is_agent: bool = Field(exclude=True)
    is_remote_access_only: bool = Field(exclude=True)

    # Foreign Key to References
    organization: OrganizationMinor = Field(exclude=True)
    type: LookupMinor = Field(exclude=True)
    user: UserMinor = Field(exclude=True)

    model_config = ConfigDict(
        extra='allow',
        from_attributes=True
    )
