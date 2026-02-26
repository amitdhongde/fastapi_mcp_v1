from typing import Annotated, Self

from datetime import date
from pydantic import (
    ConfigDict,
    Field,
    computed_field
)

# Import the project models
from modules.base.models import (
    AppBaseModelWithHashAndAuditLog
)
from modules.core.models.organization.organization import Organization

class User(AppBaseModelWithHashAndAuditLog):
    """
    User model for the application.
    """
    title: str = Field(default=None, description="Title", exclude=True)
    first_name: str = Field(default=None, description="First Name",
            exclude=True, max_length=64, examples=["John"]
        )
    middle_name: str = Field(default=None, description="Middle Name",
            exclude=True, max_length=64
        )
    last_name: str = Field(default=None, description="Last Name",
            exclude=True, max_length=64, examples=["Doe"]
        )
    avatar: str = Field(default=None, description="Avatar URL",
            exclude=True, max_length=4000
        )
    
    date_of_birth: date = Field(default=None,
            description="Date of Birth", exclude=True
        )
    gender_id: int = Field(default=0, description="Gender ID",
            exclude=True
        )
    language_id: int = Field(default=0, description="Language ID",
            exclude=True
        )

    # Foreign Key to References
    organization: Organization = Field(default=None,
            description="Organization",
            exclude=True
        )

    def __str__(self):
        return f'User: {str(self.id)} - {self.full_name}'

    @computed_field(description="Full name")
    @property
    def full_name(self) -> str:
        """
        Get the full name of the user.
        The full name is a combination of the title, first name, middle name, and last name.
        """
        return_value: str = ""
        if self.title:
            return_value += f"{self.title} "

        if self.first_name:
            return_value += f"{self.first_name} "

        if self.middle_name:
            return_value += f"{self.middle_name} "

        if self.last_name:
            return_value += f"{self.last_name}"

        if len(return_value) < 1:
            return_value = "Unknown"

        return return_value.strip()

    model_config = ConfigDict(
        extra='allow',
        populate_by_name=True,
        from_attributes=True
    )
