""" Import the required modules """

# Include the project modules
from modules.base.models.auth import AuthClaim, AccessToken
from modules.base.models.response import JsonSuccessResponse
from modules.base.helpers import TokenHelper
from modules.base.exceptions import (
        InvalidTokenException
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

    def get_token_data(self, claim: AuthClaim) -> dict:
        """
        Extracts and returns the token data from the provided AuthClaim
        instance.

        Args:
            claim (AuthClaim): An instance of AuthClaim containing the
            token data.

        Returns:
            dict: A dictionary containing the extracted token data.
        """
        token: AccessToken|None = claim.token if claim else None
        if token is None:
            raise InvalidTokenException("No access token found in the claim.")
        return TokenHelper.decode(token.access_token)

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

