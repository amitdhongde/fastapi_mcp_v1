from typing import Annotated, Self

from datetime import date
from pydantic import (
    ConfigDict, EmailStr, 
    Field
)

# Import the project models
from modules.base.models import (
    AppBaseModelWithAuditLog
)
from modules.core.models.organization import OrganizationMinor
from modules.core.models.lookup import LookupMinor
from modules.user.models import User

class Auth(AppBaseModelWithAuditLog):
    """Base model for authentication module."""

    sub: str = Field(..., 
            description="Subject identifier", max_length=255,
            examples=["auth0|1234567890"]
        ) 
    username: EmailStr | str = Field(...,
            description="Username", max_length=64, min_length=8, 
            examples=["john@someone.com"]
        )
    is_agent: bool = Field(default=False,
            description="Flag to indicate if the user is an agent"
        )
    is_remote_access_only: bool = Field(default=False,
            description="Flag to indicate if the user is remote access only"
        )

    def __str__(self):
        return f'Auth: {self.id} - {self.sub} - {self.username}'

    # @model_validator(mode='after')
    # def check_username(self) -> Self:
    #     """
    #     Validate the username field.
    #     The username can be an email or a phone number.
    #     If the username is an email, it should be a valid email address.
    #     If the username is a phone number, it should be a valid phone number.
    #     """
    #     # Check the username is for empty, email and phone number
    #     if '@' in self.username: # Email Validation
    #         ta_email = TypeAdapter(EmailStr)
    #         if not ta_email.validate_python(self.username):
    #             raise ValueError('Invalid email')
    #     elif str(self.username).isdigit(): # Phone Number Validation
    #         if len(self.username) < 10 :
    #             raise ValueError('Invalid phone number')
    #     else:
    #         raise ValueError('Invalid username')
    #     return self

    model_config = ConfigDict(
        extra='allow',
        populate_by_name=True,
        from_attributes=True
    )
