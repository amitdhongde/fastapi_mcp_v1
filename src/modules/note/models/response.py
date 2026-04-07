""" Import the required modules """
from pydantic import (
        Field
    )

# Import the project models
from modules.core.models.organization import OrganizationMinor
from modules.core.models.lookup import LookupMinor
from modules.note.models import Note

class NoteFullResponse(Note):
    """
    Note model for the application.
    """
    id: int = Field(exclude=True)
    entity_type_id: int = Field(exclude=True)

class NoteMinorResponse(Note):
    """
    Note model for the application.
    """
    id: int = Field(exclude=True)
    entity_type_id: int = Field(exclude=True)
    is_pinned: bool = Field(exclude=True)
    is_archived: bool = Field(exclude=True)

    # Foreign Key to References
    organization: OrganizationMinor = Field(exclude=True)
    entity: LookupMinor = Field(exclude=True)
