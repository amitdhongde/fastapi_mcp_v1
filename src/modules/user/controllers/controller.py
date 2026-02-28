""" Import the required modules """
from typing import List
from fastapi import Request
from pydantic import BaseModel

from ..services import UserService
from ..models import User

from modules.base.controller import BaseController
from modules.base.models.response import JsonSuccessResponse

from ..services import UserService
from ..models import User

# Include the project models
from ..models import (
    UserCreateRequest,
    UserUpdateRequest
)

class UserController(BaseController):
    def __init__(self):
        super().__init__()
        self.service = UserService()

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
            uid: str,
            request: Request,
            current_user: BaseModel) -> JsonSuccessResponse:
        """
        Get the user with the given uid.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.get(
                uid=uid,
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
            payload: UserCreateRequest,
            request: Request, current_user) -> User:
        """ Create a new user for the current user """
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
                message="User created successfully"
            )
        except Exception as e:
            raise e

    async def update(self, hash: str, payload: UserUpdateRequest) -> User:
        return await self.service.update(hash, payload)

    async def delete(self, hash: str) -> None:
        return await self.service.delete(hash)
    