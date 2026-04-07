""" Import the required modules """
from pydantic import (
    Field
)

# Include the project models
from modules.core.models.lookup import Lookup

class LookupFullResponse(Lookup):
    """
    Lookup model for the application.
    """
    order_by: int = Field(exclude=True)

class LookupMinorResponse(Lookup):
    """
    Lookup model for the application.
    """
    id: int = Field(exclude=True)
    order_by: int = Field(exclude=True)
