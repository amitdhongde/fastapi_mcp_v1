""" Import the required modules """
from pydantic import (
    ConfigDict,
    Field
)

from modules.core.models.organization import OrganizationMinor
from modules.core.models.lookup import LookupMinor
from .base import Note

class NoteFullResponse(Note):
    """
    Note model for the application.
    """
    id: int = Field(exclude=True)
    entity_type_id: int = Field(exclude=True)
    is_pinned: bool = Field(
            description="Whether the note is pinned or not",
            default=False
        )
    is_archived: bool = Field(
            description="Whether the note is archived or not",
            default=False
        )

    # Foreign Key to References
    organization: OrganizationMinor = Field(
            description="Organization",
            exclude=False
        )
    entity: LookupMinor = Field(
            description="Entity Type",
            exclude=False
        )

    model_config = ConfigDict(
        extra='allow',
        from_attributes=True
    )

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

    model_config = ConfigDict(
        extra='allow',
        from_attributes=True
    )
