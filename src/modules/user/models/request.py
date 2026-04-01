""" Import the required modules """
import datetime
import time
from typing_extensions import Self
from pydantic import (
    BaseModel, Field, model_validator
)

class UserBaseModel(BaseModel):
    """
    User model for the application.
    """
    title: str = Field(default=None, description="Title of the user.",
            examples=["Mr.", "Mrs.", "Dr."], max_length=64,
            json_schema_extra={"nullable": False}
        )
    first_name: str = Field(default=None, description="First Name of the user.",
            examples=["John"], max_length=64,
            json_schema_extra={"nullable": False}
        )
    middle_name: str = Field(default=None, description="Middle Name of the user.",
            max_length=64, json_schema_extra={"nullable": True}
        )
    last_name: str = Field(default=None, description="Last Name of the user.",
            examples=["Doe"], max_length=64,
            json_schema_extra={"nullable": False}
        )

    @model_validator(mode='after')
    def check_first_name(self) -> Self:
        """
        Validate the first_name field to check if it is not empty.
        """
        if not self.first_name or self.first_name.strip() == "":
            raise ValueError('First Name cannot be empty')
        return self

# Define the Create model
class UserCreateRequest(UserBaseModel):
    """
    Model for user create request.
    """
    pass

# Define the Update model
class UserUpdateRequest(UserBaseModel):
    """
    Model for user update request.
    """
    pass
