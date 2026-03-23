""" Import the required modules """
from typing import List
from fastapi import Request
from pydantic import BaseModel

from modules.base.controller import BaseController
from modules.base.models.response import JsonSuccessResponse

from ..services import NoteService
from ..models import Note

# Include the project models
from ..models import (
    NoteCreateRequest,
    NoteUpdateRequest
)

class NoteController(BaseController):
    def __init__(self):
        super().__init__()
        self.service = NoteService()
    
    async def index(
            self,
            commons: dict,
            request: Request,
            current_user: BaseModel) -> JsonSuccessResponse:
        """
        Get all the users.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.list(
                commons=commons,
                request=request,
                ip_address=ip_address
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
            ip_address = request.client.host

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
            ip_address = request.client.host

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
