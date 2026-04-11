""" Import the required modules """
from pydantic import (
        ConfigDict,
        computed_field
    )

# Include the project models
from modules.base.models import CustomBaseModel
from .token import Token as AuthToken

class AuthClaim(CustomBaseModel):
    """
    AuthClaim model for the application.
    This model is used to store the authentication claim for a user.
    It contains the token, auth data, privileges, settings, and unread notifications.
    """
    model_config = ConfigDict(
            extra='allow'
        )

    token: AuthToken | None = None
    auth: dict = {}

    @computed_field(description="Claim ID")
    @property
    def key(self) -> str | None:
        if self.token is None:
            return None
        return self.token.access_token

    @computed_field(description="Claim TTL")
    @property
    def ttl(self) -> int:
        if self.token is None:
            return 0
        return self.token.expires_at
