""" Import the required modules """
from abc import ABC

# Include the project models
from modules.base.models import CustomBaseModel
from modules.base.models.auth import AuthClaim, AccessToken
from modules.base.services.auth import ClaimService

from modules.base.exceptions.base import InvalidTokenException

class BaseService(ABC):
    """Base class for services."""
    def __init__(self, repository=None):
        self.repository = repository
        self.claim_service = ClaimService()

    def get_data(self, claim: CustomBaseModel) -> dict:
        """Extracts and returns the token data from the provided CustomBaseModel
        instance.

        Args:
            claim (CustomBaseModel): An instance of CustomBaseModel containing the
            token data.

        Returns:
            dict: A dictionary containing the extracted token data.
        """
        if isinstance(claim, AuthClaim):
            token: AccessToken|None = claim.token if claim else None
            if token is None:
                raise InvalidTokenException("No access token found in the claim.")
            return self.claim_service.decode(token.access_token)
        return {}

