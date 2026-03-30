""" Import the required modules """
from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Include the project models
from modules.base.models.auth import AuthClaim
from modules.user.models import UserAuthModel

# Include the project services
from modules.base.services.auth.claim_service import ClaimService

# Include the project exceptions
from modules.base.exceptions import (
    InvalidTokenException,
    AuthenticationException
)

class AuthGaurd:
    access_token: str | None = None

    def __init__(
        self,
        token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer(auto_error=False))],
        claim_service: ClaimService = Depends(ClaimService)
    ):
        """ Initialize the AuthGaurd with the provided token and claim service.
        This class is used to validate the access token and retrieve the user
        associated with the token. If the token is not provided or invalid,
        an InvalidTokenException is raised.
        Args:
            token (HTTPAuthorizationCredentials): The access token provided in the request.
            claim_service (ClaimService): The service to handle claims and user retrieval.
        """
        try :
            if not token:
                raise InvalidTokenException(
                    error_msg_code="error_code_claim_not_found"
                )
            self.access_token = token.credentials
            self.claim_service = claim_service

            # Validate the token during initialization
            self.valid_token()
        except Exception as e:
            raise e

    def valid_token(self)-> str:
        """
        Validate the access token and return it if valid.
        Raise an exception if invalid.
        """
        try:
            # This could be JWT validation.
            self.get_claim()

            # Token validation logic can be added here (e.g., check expiration, issuer, etc.)
            payload: dict = self.get_token_data()
            if payload is None:
                raise InvalidTokenException(
                    error_msg_code="error_code_invalid_token"
                )

            return self.access_token
        except (InvalidTokenException, AuthenticationException, Exception) as e:
            raise e

    def get_token(self) -> str:
        return self.access_token

    def get_user(self) -> UserAuthModel:
        try:
            # This could be JWT validation.
            claim: AuthClaim = self.get_claim()

            auth_data: dict = claim.auth
            if "user" in auth_data:
                user_data = auth_data["user"]
                user: UserAuthModel = UserAuthModel.model_validate(user_data)
            else:
                raise AuthenticationException(
                    error_msg_code="error_code_user_not_found_in_claim"
                )
            return user
        except (AuthenticationException, Exception) as e:
            raise e

    def get_claim(self) -> AuthClaim:
        try:
            claim: AuthClaim = self.claim_service.get(value=self.access_token)
            if claim is None:
                raise AuthenticationException(
                    error_msg_code="error_code_claim_not_found"
                )
            return claim
        except (AuthenticationException, Exception) as e:
            raise e

    def get_token_data(self) -> dict:
        try:
            return self.claim_service.decode(self.access_token)
        except Exception as e:
            raise e

    @property
    def authorize(self, required_privileges: list[str]) -> bool:
        """
        Authorize the user based on the required privileges.
        Return True if authorized, False otherwise.
        """
        try:
            print("Required Privileges:", required_privileges)
            # claim: AuthClaim = self.get_claim()
            # user_privileges: list[str] = claim.privileges

            # # Check if any of the required privileges are in the user's privileges
            # for privilege in required_privileges:
            #     if privilege in user_privileges:
            #         return True

            return False
        except Exception as e:
            raise e

    def __call__(self,
            request: Annotated[
                HTTPAuthorizationCredentials,
                Depends(HTTPBearer(auto_error=False))
            ]
        ) -> str:
        print("AuthGaurd __call__ with token:", request)
        return self.valid_token()


    # async def valid_token(self, token: str) -> str:
    #     try:
    #         # This could be JWT validation, looking up a session token in the DB, etc.
    #         return token
    #     except Exception as e:
    #         raise InvalidTokenException(message=str(e)) from e


    # async def get_user_for_token(token: str):
    #     return await User(1, "Amit", "amit@gmail.com")


    # async def validate_user(self):
        # try:
        #     user = await self.get_user_for_token(self.access_token)
        #     if user == None:
        #         raise HTTPException(status_code=401, detail="Unauthorized")
        #     return user
        # except:
        #     raise HTTPException(status_code=401, detail="Unauthorized")

        # class TokenGuard_ValidUser(TokenGaurd_ValidToken):

        #     async def __call__(self, request: Request = Depends(Request)):
        #         user = await self.validate_user(request)
        #         return user

        # class TokenGuard_ValidPermissions(TokenGaurd_ValidToken):

        #     async def __call__(self, request: Request = Depends(Request)):
        #         user = await self.validate_permissions(request)
        #         return user

auth = AuthGaurd
