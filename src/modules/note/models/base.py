from typing import Annotated, Self

from pydantic import (
    ConfigDict, Field
)

# Import the project models
from modules.base.models import AppBaseModelWithHashAndAuditLog
from modules.core.models.organization.organization import Organization

class Note(AppBaseModelWithHashAndAuditLog):
    """
    Note model for the application.
    """
    entity_type_id: int = Field(default=0, description="Type of the entity.",
            json_schema_extra={"nullable": False}
        )
    reference_id: int = Field(default=0, description="ID of the reference entity.",
            json_schema_extra={"nullable": False}
        )
    title: str = Field(default=None, description="Title of the note.",
            examples=["Meeting Notes", "Project Update"],
            json_schema_extra={"nullable": False}
        )
    content: str = Field(default=None, description="Text content of the note.",
            examples=["This is a note."],
            json_schema_extra={"nullable": False}
        )

    def __str__(self):
        return f'Note: {str(self.id)} - {self.note}'

    model_config = ConfigDict(
        extra='allow',
        populate_by_name=True,
        from_attributes=True
    )
