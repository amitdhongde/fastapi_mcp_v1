""" Import the required modules """
from typing import List
from starlette.requests import Request
from pydantic import BaseModel
import logging

from modules.base.controller import BaseController
from modules.base.models.response import JsonSuccessResponse
from modules.base.fastapi.dependencies.authentication import (
        AuthGuard
    )

from ..services import NoteService
from ..models import Note

# Include the project models
from ..models import (
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

    async def index(
            self,
            commons: dict,
            request: Request,
            guard: AuthGuard) -> JsonSuccessResponse:
        """
        Get all the users.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host if request is not None else "0.0.0.0"

            response: BaseModel = await self.service.list(
                    commons=commons,
                    request=request,
                    ip_address=ip_address,
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
            hash: str,
            request: Request,
            current_user: BaseModel) -> JsonSuccessResponse:
        """
        Get the user with the given hash.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host if request is not None else "0.0.0.0"

            response: BaseModel = await self.service.get(
                hash=hash,
                ip_address=ip_address
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
            current_user: BaseModel) -> JsonSuccessResponse:
        """ Create a new note for the current user """
        try:
            # Get the ip address from the request
            ip_address = request.client.host if request is not None else "0.0.0.0"

            # Convert the payload to dict
            payload = payload.model_dump()

            response: BaseModel = await self.service.create(
                payload, ip_address,
                current_user
            )

            # Send data from the service
            return JsonSuccessResponse(
                content=response,
                message="Note created successfully"
            )
        except Exception as e:
            raise e

    async def update(
            self, hash: str, 
            payload: NoteUpdateRequest,
            request: Request,
            current_user: BaseModel) -> Note:
        return await self.service.update(hash, payload)

    async def delete(
            self, hash: str,
            request: Request,
            current_user: BaseModel) -> None:
        return await self.service.delete(hash)
