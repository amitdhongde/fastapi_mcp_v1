""" Import the required modules """
from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)

# Include the project models
from modules.core.models.lookup import Lookup

class LookupRequest(BaseModel):
    """
    Lookup model for the application.
    """
    order_by: int = Field(exclude=True)

    model_config = ConfigDict(
        extra='allow',
        from_attributes=True
    )

class LookupCreateRequest(Lookup):
    """
    Lookup model for the application.
    """
    order_by: int = Field(exclude=True)

    model_config = ConfigDict(
        extra='allow',
        from_attributes=True
    )

class LookupUpdateRequest(LookupRequest):
    """
    Lookup model for the application.
    """
    model_config = ConfigDict(
        extra='allow',
        from_attributes=True
    )
