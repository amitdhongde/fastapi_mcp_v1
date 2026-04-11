""" Import the required modules """
import logging
from typing import List
from starlette.requests import Request
from pydantic import TypeAdapter

# Include the project models
from modules.base.models import CustomBaseModel
from modules.note.models import (
        NoteUpdateRequest,
        NoteFullResponse,
        NoteMinorResponse
    )

# include the project services
from modules.base.services.base import BaseService

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
        super().__init__(self.repository)

    async def create(
            self, payload: dict,
            request: Request,
            claim: CustomBaseModel) -> NoteFullResponse:
        """ Create a new object """
        try :
            # Validate the credentials
            response = await self.repository.create(
                    payload,
                    self.get_data(claim).get('user_id')
                )

            if not response:
                raise EntityNotSavedException(
                    message="Unable to create the note"
                )

            # Validate the response
            model: NoteFullResponse = \
                TypeAdapter(NoteFullResponse).validate_python(response)

            # Raise event on successful creation
            NoteCreatedEvent().raise_event(model)

            return model
        except Exception as e:
            raise e

    async def update(
            self, uid: str,
            payload: NoteUpdateRequest,
            request: Request,
            claim: CustomBaseModel) -> NoteFullResponse:
        """ Update the model """
        try:
            # Set local variable for the payload
            user_id: int = self.get_data(claim).get('user_id')

            # Build the conditions for the query
            conditions = {}
            if user_id is not None:
                conditions["created_by"] = user_id

            # Get the claim from storage
            response = await self.repository.update_by_uid(
                    uid, payload,
                    conditions=conditions,
                    updated_by=user_id
                )
            if not response:
                raise EntityNotSavedException(
                    message="Unable to update the note"
                )

            # Validate the response
            model: NoteFullResponse = \
                TypeAdapter(NoteFullResponse).validate_python(response)

            # Raise event on successful update
            NoteUpdatedEvent().raise_event(model)

            return model
        except Exception as e:
            raise e

    async def delete(
            self, uid: str,
            request: Request,
            claim: CustomBaseModel) -> NoteFullResponse:
        """ Delete the model """
        try:
            # Set local variable for the payload
            user_id: int = self.get_data(claim).get('user_id')

            # Build the conditions for the query
            conditions = {}
            if user_id is not None:
                conditions["created_by"] = user_id

            response = await self.repository.delete_by_uid(
                    uid,
                    conditions=conditions,
                    deleted_by=user_id
                )
            if not response:
                raise EntityNotFoundException(
                    message="Unable to delete the note"
                )

            # Validate the response
            model: NoteFullResponse = \
                TypeAdapter(NoteFullResponse).validate_python(response)

            # Raise event on successful deletion
            NoteDeletedEvent().raise_event(model)

            return model
        except Exception as e:
            raise e

    async def list(
            self,
            commons: dict,
            request: Request,
            claim: CustomBaseModel
        ) -> List[NoteMinorResponse]:
        """ List all the objects """
        try:
            # Set local variable for the payload
            user_id: int = self.get_data(claim).get('user_id')

            # Get the ip address from the request
            ip_address = request.client.host if request is not None else "0.0.0.0"

            # Create conditions for the query
            conditions = {}
            if user_id is not None:
                conditions["created_by"] = user_id

            # Conditions for the query
            if commons.get("q") is not None:
                _query: list[str] = commons.get("q", {})
                for data in _query:
                    field, value = data.split("=")
                    conditions[field] = value

            # Validate the payload
            response = await self.repository.get_all(
                    skip=commons.get("skip", 0),
                    limit=commons.get("limit", 100),
                    conditions=conditions
                )
            if not response:
                raise EntityNotFoundException(
                    message="Unable to get the notes from IP address."
                )

            # Validate the response
            models: List[NoteMinorResponse] = \
                TypeAdapter(List[NoteMinorResponse]).validate_python(response)

            return models
        except Exception as e:
            raise e

    async def get(
            self,
            uid: str,
            request: Request,
            claim: CustomBaseModel) -> NoteFullResponse:
        """ Get the object """
        try:
            # Set local variable for the payload
            user_id: int = self.get_data(claim).get('user_id')

            # Create conditions for the query
            conditions = {}
            if user_id is not None:
                conditions["created_by"] = user_id

            # Validate the payload
            response = await self.repository.get_by_hash(uid, conditions=conditions)
            if not response:
                raise EntityNotFoundException(
                    message="Unable to get the note"
                )

            # Validate the response
            model: NoteFullResponse = \
                TypeAdapter(NoteFullResponse).validate_python(response)

            return model
        except Exception as e:
            raise e
