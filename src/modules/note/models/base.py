""" Import the required modules """
from pydantic import (
        Field
    )

# Import the project models
from modules.base.models import AppBaseModelWithHashAndAuditLog
from modules.core.models.organization import OrganizationMinor
from modules.core.models.lookup import LookupMinor

class Note(AppBaseModelWithHashAndAuditLog):
    """
    Note model for the application.
    """
    entity_type_id: int = Field(default=0, description="Type of the entity."
        )
    reference_id: int = Field(default=0, description="ID of the reference entity."
        )
    title: str = Field(default=None, description="Title of the note.",
            examples=["Meeting Notes", "Project Update"],
            max_length=128
        )
    content: str = Field(default=None, description="Text content of the note.",
            examples=["This is a note."],
            max_length=8000
        )
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

    def __str__(self):
        return f'Note: {str(self.id)} - {self.title}'
