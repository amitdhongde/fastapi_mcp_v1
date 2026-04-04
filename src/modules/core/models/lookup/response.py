""" Import the required modules """
from pydantic import (
    ConfigDict,
    Field
)

# Include the project models
from modules.core.models.lookup import Lookup

class LookupFullResponse(Lookup):
    """
    Lookup model for the application.
    """
    order_by: int = Field(exclude=True)

    model_config = ConfigDict(
        extra='allow',
        from_attributes=True
    )

class LookupMinorResponse(Lookup):
    """
    Lookup model for the application.
    """
    id: int = Field(exclude=True)
    order_by: int = Field(exclude=True)

    model_config = ConfigDict(
        extra='allow',
        from_attributes=True
    )
