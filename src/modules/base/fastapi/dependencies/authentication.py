""" Import the required modules """
from typing import Annotated

from fastapi import Depends
from fastapi.security import (
        HTTPAuthorizationCredentials,
        HTTPBearer, OAuth2PasswordBearer
    )

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

# Define the OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_auth_guard(
        token: Annotated[str, Depends(oauth2_scheme)],
        guard: Annotated[AuthGuard, Depends()],
    ) -> AuthGuard:
    """ Dependency to extract and validate the access token from the request.
    This function uses the OAuth2PasswordBearer to extract the token from the
    Authorization header and then validates it using the AuthGuard. If the token
    is valid, it returns the AuthGuard instance; otherwise, it raises an
    InvalidTokenException.
    Args:
        token (str): The access token extracted from the Authorization header.
        guard (AuthGuard): The AuthGuard instance used to validate the token.
    Returns:
        AuthGuard: The AuthGuard instance if the token is valid.
    Raises:
        InvalidTokenException: If the token is invalid or not provided.
    """
    if guard.valid_token() != token:
        raise InvalidTokenException(
            error_msg_code="error_code_invalid_token"
        )
    return guard

class AuthGuard:
    """ AuthGuard is a dependency class used to validate access tokens and retrieve
    user information from the token. It uses the ClaimService to decode the token
    and extract the claims, which include user information. If the token is valid,
    it allows access to the protected routes; otherwise, it raises an exception.
    """
    access_token: str | None = None

    def __init__(
        self,
        token: Annotated[
                HTTPAuthorizationCredentials,
                Depends(HTTPBearer(auto_error=False))
            ],
        claim_service: ClaimService = Depends(ClaimService)
    ):
        """ Initialize the AuthGuard with the provided token and claim service.
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

    def get_token_value(self, key: str) -> any:
        return self.get_token_data().get(key)

    def __call__(self,
            request: Annotated[
                HTTPAuthorizationCredentials,
                Depends(HTTPBearer(auto_error=False))
            ]
        ) -> str:
        print("AuthGuard __call__ with token:", request)
        return self.valid_token()
