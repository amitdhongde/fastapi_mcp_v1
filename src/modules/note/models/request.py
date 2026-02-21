""" Import the required modules """
import datetime
import time
from typing_extensions import Self
from pydantic import (
    BaseModel, Field, model_validator
)

class NoteBaseModel(BaseModel):
    """
    Base model for note models.
    """
    title: str = Field(default=None, description="Title of the note.",
            examples=["Meeting Notes", "Project Update"],
            nullable=False
        )
    content: str = Field(default=None, description="Text content of the note.",
            examples=["This is a note."], max_length=8000,
            nullable=False
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
        if not self.content or self.content.strip() == "":
            raise ValueError('Content cannot be empty')
        return self

# Define the Create model
class NoteCreateRequest(NoteBaseModel):
    """
    Model for note create request.
    """
    pass

class NoteUpdateRequest(NoteBaseModel):
    """
    Model for note update request.
    """
    pass
