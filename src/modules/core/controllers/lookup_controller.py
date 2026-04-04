""" Import the required modules """
from fastapi import Request
from pydantic import BaseModel

# Include the project modules
from modules.base.models.response import JsonSuccessResponse
from modules.base.controller.base import BaseController
from modules.base.fastapi.dependencies.authentication import (
        AuthGuard
    )

# Include the project services
from modules.core.services import LookupService

class LookupController(BaseController):
    """
    LookupController class to handle lookup related requests.
    This class inherits from the BaseController class and uses the 
    LookupService
    """

    def __init__(self):
        super().__init__()
        self.service = LookupService()

    async def index(
            self,
            commons: dict,
            request: Request,
            guard: AuthGuard) -> JsonSuccessResponse:
        """
        Get all the lookup values.
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
        Get the lookup with the given uid.
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
            payload: BaseModel,
            request: Request,
            guard: AuthGuard) -> JsonSuccessResponse:
        """
        Create a new lookup with the given payload.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.create(
                payload, ip_address, guard
            )

            # Send data from the service
            return JsonSuccessResponse(
                content=response
            )
        except Exception as e:
            raise e


    async def update(
            self,
            uid: str,
            payload: BaseModel,
            request: Request,
            guard: AuthGuard) -> JsonSuccessResponse:
        """
        Update the lookup with the given uid and payload.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.update(
                uid=uid,
                payload=payload,
                ip_address=ip_address,
                guard=guard
            )

            # Send data from the service
            return JsonSuccessResponse(
                content=response
            )
        except Exception as e:
            raise e


    async def delete(
            self,
            uid: str,
            request: Request,
            guard: AuthGuard) -> JsonSuccessResponse:
        """
        Delete the lookup data with the given uid.
        """
        try:
            # Get the ip address from the request
            ip_address = request.client.host

            response: BaseModel = await self.service.delete(
                uid=uid,
                ip_address=ip_address,
                guard=guard
            )

            # Send data from the service
            return JsonSuccessResponse(
                content=response
            )
        except Exception as e:
            raise e
