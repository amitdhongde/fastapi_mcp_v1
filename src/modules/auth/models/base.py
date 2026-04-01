""" Import the required modules """
from pydantic import (
    ConfigDict, EmailStr,
    Field
)

# Import the project models
from modules.base.models import (
        AppBaseModelWithAuditLog
    )

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

    model_config = ConfigDict(
        extra='allow',
        populate_by_name=True,
        from_attributes=True
    )
