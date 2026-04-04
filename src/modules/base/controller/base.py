""" Import the required modules """
from fastapi import Request
from pydantic import BaseModel

# Include the project modules
from modules.base.models.response import JsonSuccessResponse
from modules.base.fastapi.dependencies.authentication import (
        AuthGuard
    )

class BaseController():
    """
    BaseController class to handle common functionality for all 
    controllers.
    """
    def __init__(self) -> None:
        """
        Initializes a new instance of the BaseController class with no
        additional setup.
        """
        pass

    # async def show(
    #         self,
    #         uid: str,
    #         request: Request,
    #         guard: AuthGuard) -> JsonSuccessResponse:
    #     """
    #     Get the lookup with the given uid.
    #     """
    #     try:
    #         # Get the note from the service
    #         response: BaseModel = await self.service.get(
    #             uid=uid,
    #             request=request,
    #             guard=guard
    #         )

    #         # Send data from the service
    #         return JsonSuccessResponse(
    #             content=response
    #         )
    #     except Exception as e:
    #         raise e

