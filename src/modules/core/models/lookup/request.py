""" Import the required modules """
from pydantic import (
    ConfigDict,
    Field
)

# Include the project models
from modules.base.models import CustomBaseModel

class LookupRequest(CustomBaseModel):
    """
    Lookup model for the application.
    """
    model_config = ConfigDict(
            extra='allow',
        )

    order_by: int = Field(exclude=True)

class LookupCreateRequest(LookupRequest):
    """
    Lookup model for the application.
    """

class LookupUpdateRequest(LookupRequest):
    """
    Lookup model for the application.
    """
