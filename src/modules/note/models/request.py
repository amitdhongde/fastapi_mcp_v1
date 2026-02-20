""" Import the required modules """
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
    note: str = Field(default=None, description="Text content of the note.",
            examples=["This is a note."], max_length=8000,
            nullable=False
        )

    @model_validator(mode='after')
    def check_title(self) -> Self:
        """
        Validate the title field to check if it is not empty.
        """
        if not self.title or self.title.strip() == "":
            self.title = "Untitled Note"
        return self

    @model_validator(mode='after')
    def check_note(self) -> Self:
        """
        Validate the note field to check if it is not empty.
        """
        if not self.note or self.note.strip() == "":
            raise ValueError('Note cannot be empty')
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
