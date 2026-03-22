from pydantic import (
    ConfigDict,
    Field,
    computed_field
)

from modules.core.enums import LookupMaster

# Import the project models
from modules.base.models import (
    ApplicationBaseModel,
    AppBaseModelWithHashAndAuditLog
)
from modules.core.models.lookup import LookupMinor

class User(AppBaseModelWithHashAndAuditLog):
    """
    User model for the application.
    """
    title: str|None = Field(default=None, description="Title", exclude=True)
    first_name: str = Field(default=None, description="First Name",
            exclude=True, max_length=64, examples=["John"]
        )
    middle_name: str|None = Field(default=None, description="Middle Name",
            exclude=True, max_length=64
        )
    last_name: str|None = Field(default=None, description="Last Name",
            exclude=True, max_length=64, examples=["Doe"]
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

class UserMinor(User):
    """
    User minor response model for the application.
    This model is used for responses where only basic user information is required.
    """
    id: int = Field(exclude=True)

class UserDetail(ApplicationBaseModel):
    """
    User Detail model for the application.
    This model is used to store additional details about the user.
    """
    organization_id: int = Field(exclude=True)
    user_id: int = Field(exclude=True)
    identifier: str = Field(exclude=False)
    proxy: str|None = Field(default=None, exclude=False)
    is_primary: bool = Field(default=False, description="Is Primary", exclude=False)
    is_verified: bool = Field(default=False, description="Is Verified", exclude=False)
    is_secure: bool = Field(default=False, description="Is Secure", exclude=False)

    # Relationships
    type: LookupMinor = Field(
            description="User Type", exclude=False
        )
    subtype: LookupMinor|None = Field(
            description="User Subtype", exclude=False
        )

    # Identifier output field
    @computed_field(description="Identifier display")
    @property
    def identifier_output(self) -> str:
        """
        Get the identifier output.
        If the identifier is an email, it will be masked for security reasons.
        """
        return_value: str = self.identifier

        # If the detail is marked as secure, we will mask the identifier based on its type
        if (self.is_secure == True) and (self.type is not None) \
            and (self.type.lookup_type == LookupMaster.USER_DETAIL_TYPE):
            match self.type.lookup_key:
                case "user_detail_type_email": # Email
                    # Mask the email address except for the first
                    # and last character of the local part
                    local_part, domain_part = self.identifier.split("@")
                    if len(local_part) > 4:
                        masked_local_part = local_part[:2] + ((len(local_part)-4) * "*") + local_part[-2:]
                    else:
                        masked_local_part = len(local_part) * "*"
                    return_value = f"{masked_local_part}@{domain_part}"
                case "user_detail_type_phone": # Phone
                    # Mask the phone number except for the first 2 and
                    # last 2 digits, omit the first + character if present
                    if self.identifier.startswith("+"):
                        masked_phone = "+" + self.identifier[1:3] + ((len(self.identifier)-5) * "*") + self.identifier[-2:]
                    else:
                        masked_phone = self.identifier[:2] + ((len(self.identifier)-4) * "*") + self.identifier[-2:]
                    return_value = masked_phone
                case _:
                    # Mask the identifier except for the first and last character
                    if len(self.identifier) > 2:
                        return_value = self.identifier[0] + "****" + self.identifier[-1]
                    else:
                        return_value = self.identifier

            return return_value
        else:
            return_value = self.identifier

        return return_value
