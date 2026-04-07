""" Import the required modules """
import datetime
import time
from typing_extensions import Self
from pydantic import (
        Field,
        model_validator
    )

# Include the project models
from modules.base.models import CustomBaseModel

class NoteBaseModel(CustomBaseModel):
    """
    Base model for note models.
    """
    entity_type_id: int = Field(default=0, description="Type of the entity."
        )
    reference_id: int = Field(default=0, description="ID of the reference entity.",
            examples=[1], le=1
        )
    title: str = Field(default=None, description="Title of the note.",
            examples=["Meeting Notes", "Project Update"],
            max_length=128
        )
    content: str = Field(default=None, description="Text content of the note.",
            examples=["This is a note."],
            max_length=8000
        )

    @model_validator(mode='after')
    def check_title(self) -> Self:
        """
        Validate the title field to check if it is not empty.
        """
        if not self.title or self.title.strip() == "":
            # UTC time to the second
            current_date = datetime.date.fromtimestamp(time.time())

            # If the title is empty, set it to "Untitled Note" with the current timestamp
            self.title = f"Untitled Note - {current_date.isoformat()}"

        return self

    @model_validator(mode='after')
    def check_content(self) -> Self:
        """
        Validate the content field to check if it is not empty.
        """
        if not self.content:
            raise ValueError('Content cannot be empty')
        return self

# Define the Create model
class NoteCreateRequest(NoteBaseModel):
    """
    Model for note create request.
    """
    reference_id: int = Field(default=0, description="Reference Id of the entity.",
            le=1
        )

class NoteUpdateRequest(NoteBaseModel):
    """
    Model for note update request.
    """
