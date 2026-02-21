""" Import the required modules """
import logging
from typing import List
from fastapi import Request
from pydantic import TypeAdapter, BaseModel

# Include the project models
from modules.note.models import (
    NoteCreateRequest,
    NoteUpdateRequest
)
from modules.note.models import Note

# include the project services
from modules.base.services.base import BaseService
from modules.base.services.auth.claim_service import ClaimService

# Include the module repositories
from modules.note.repositories import NoteRepository

# Include the module exceptions
from modules.base.exceptions.base import (
    EntityNotFoundException,
    EntityNotSavedException
)

# Include the module events
from ..events import (
    NoteCreatedEvent,
    NoteUpdatedEvent,
    NoteDeletedEvent
)

# Initialize the logger
logger = logging.getLogger(__name__)

class NoteService(BaseService):
    """ Service class to handle all note related operations. """
    def __init__(self):
        self.repository = NoteRepository()
        self.claim_service = ClaimService()
        super().__init__(self.repository)

    async def create(
            self, payload: dict, ip_address: str,
            current_user: BaseModel) -> Note:
        """ Create a new object """
        try :
            print(payload)
            # add the user id to the payload
            payload["organization_id"] = 1

            # Validate the credentials
            response = await self.repository.create(
                payload
            )

            if not response:
                raise EntityNotSavedException(
                    message="Unable to create the note"
                )

            # Validate the response
            model: Note = TypeAdapter(Note).validate_python(response)

            # Raise event on successful creation
            NoteCreatedEvent().raise_event(model)

            return model
        except Exception as e:
            raise e

    async def update(
            self, uid: str, payload: NoteUpdateRequest,
            ip_address: str, current_user: BaseModel) -> Note:
        """ Update the model """
        try:
            # Get the claim from storage
            response = await self.repository.update_by_hash(
                uid, payload, ip_address, current_user
            )
            if not response:
                raise EntityNotSavedException(
                    message="Unable to update the note"
                )

            # Validate the response
            model: Note = TypeAdapter(Note).validate_python(response)

            # Raise event on successful update
            NoteUpdatedEvent().raise_event(model)

            return model
        except Exception as e:
            raise e

    async def delete(
            self, uid: str, ip_address: str,
            current_user: BaseModel) -> Note:
        """ Delete the model """
        try:
            response = await self.repository.delete_by_hash(
                uid, ip_address, current_user
            )
            if not response:
                raise EntityNotFoundException(
                    message="Unable to delete the note"
                )

            # Validate the response
            model: Note = TypeAdapter(Note).validate_python(response)

            # Raise event on successful deletion
            NoteDeletedEvent().raise_event(model)            

            return model
        except Exception as e:
            raise e

    async def list(
            self,
            commons: dict,
            request: Request,
            ip_address: str
        ) -> List[Note]:
        """ List all the objects """
        try:
            # Validate the payload
            response = await self.repository.get_all(
                skip=commons.get("skip", 0),
                limit=commons.get("limit", 100),
            )
            logger.debug(f"Note count: {len(response)}")
            if not response:
                raise EntityNotFoundException(
                    message="Unable to get the notes from IP address."
                )
            
            # Validate the response
            models: List[Note] = TypeAdapter(List[Note]).validate_python(response)

            return models
        except Exception as e:
            raise e

    async def get(
            self,
            uid: str,
            ip_address: str
        ) -> Note:
        """ Get the object """
        try:
            # Validate the payload
            response = await self.repository.get_by_hash(uid)
            if not response:
                raise EntityNotFoundException(
                    message="Unable to get the note from IP address = " + ip_address
                )

            # Validate the response
            model: Note = TypeAdapter(Note).validate_python(response)

            return model
        except Exception as e:
            raise e
