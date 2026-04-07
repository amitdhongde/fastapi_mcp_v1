""" Import the required modules """
from pydantic import (
        ConfigDict, Field
    )

# Include the project models
from modules.base.models import CustomBaseModel

class OrganizationBaseModel(CustomBaseModel):
    """
    Base model for organization models.
    """
    model_config = ConfigDict(
            extra='allow',
        )

    display_name: str = Field(default=None, description="Display Name",
            max_length=128, examples=["My Organization"]
        )
    legal_name: str = Field(default=None, description="Legal Name",
            exclude=True, max_length=128,
            examples=["My Organization Inc"]
        )

# Define the Create model
class OrganizationCreateRequest(OrganizationBaseModel):
    """
    Model for organization create request.
    """

class OrganizationUpdateRequest(OrganizationBaseModel):
    """
    Model for organization update request.
    """
