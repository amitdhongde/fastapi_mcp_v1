""" Import the required modules """
import logging
from starlette.requests import Request
from pydantic import BaseModel

# Include the project dependencies
from modules.base.controller import BaseController
from modules.base.models.response import JsonSuccessResponse
from modules.base.fastapi.dependencies.authentication import (
        AuthGuard
    )
from modules.note.services import NoteService
from modules.core.services import LookupService
from modules.core.models.lookup import LookupFullResponse

# Include the project models
from modules.note.models import (
    NoteCreateRequest,
    NoteUpdateRequest
)

# Initialize the logger
logger = logging.getLogger(__name__)

class NoteController(BaseController):
    """ Controller class to handle all note related actions. """
    def __init__(self):
        super().__init__()
        self.service = NoteService()
        self.lookup_service = LookupService()

    async def index(
            self,
            commons: dict,
            request: Request,
            guard: AuthGuard) -> JsonSuccessResponse:
        """
        Get all the notes.
        """
        try:
            # Get the list of notes from the service
            response: BaseModel = await self.service.list(
                    commons=commons,
                    request=request,
                    guard=guard
                )

            # Send data from the service
            return JsonSuccessResponse(
                    content=response
                )
        except Exception as e:
            raise e

    async def show(
            self,
            uid: str,
            request: Request,
            guard: AuthGuard) -> JsonSuccessResponse:
        """
        Get the note with the given uid.
        """
        try:
            # Get the note from the service
            response: BaseModel = await self.service.get(
                uid=uid,
                request=request,
                guard=guard
            )

            # Send data from the service
            return JsonSuccessResponse(
                content=response
            )
        except Exception as e:
            raise e

    async def create(
            self,
            payload: NoteCreateRequest,
            request: Request,
            guard: AuthGuard) -> JsonSuccessResponse:
        """ Create a new note for the current user """
        try:
            # Fetch the entity_type from request context
            entity_type = request.scope.get("entity_type", "entity_type_organization")
            entity_type_lookup: LookupFullResponse = await self.lookup_service.get_by_key(
                    key=entity_type
                )

            # Convert the payload to dict
            payload = payload.model_dump()

            # Add the additional information to the payload
            payload["organization_id"] = guard.get_token_value('org_id')
            payload["entity_type_id"] = entity_type_lookup.id

            response: BaseModel = await self.service.create(
                payload,
                request=request,
                guard=guard
            )

            # Send data from the service
            return JsonSuccessResponse(
                content=response,
                message="Note created successfully"
            )
        except Exception as e:
            raise e

    async def update(
            self, uid: str,
            payload: NoteUpdateRequest,
            request: Request,
            guard: AuthGuard) -> JsonSuccessResponse:
        """ Update the note with the given uid """
        try:
            # Convert the payload to dict
            payload = payload.model_dump()

            response: BaseModel = await self.service.update(
                    uid,
                    payload,
                    request=request,
                    guard=guard
                )

            # Send data from the service
            return JsonSuccessResponse(
                content=response,
                message="Note updated successfully"
            )
        except Exception as e:
            raise e

    async def delete(
            self, uid: str,
            request: Request,
            guard: AuthGuard) -> JsonSuccessResponse:
        """ Delete the note with the given uid """
        try:
            response: BaseModel = await self.service.delete(
                    uid,
                    request=request,
                    guard=guard
                )

            # Send data from the service
            return JsonSuccessResponse(
                    content=response,
                    message="Note deleted successfully"
                )
        except Exception as e:
            raise e
