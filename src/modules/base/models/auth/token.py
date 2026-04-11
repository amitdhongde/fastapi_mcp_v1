""" Import the required modules """
from datetime import datetime, timezone
from pydantic import ConfigDict, PositiveInt

# Include the project models
from modules.base.models import CustomBaseModel

class Token(CustomBaseModel):
    """Token model for the application.
    This model is used to store the authentication token for a user.
    It contains the access token, token type, refresh token, id token,
    created at, and expires at.
    """
    model_config = ConfigDict(
            extra='forbid'
        )
    access_token: str | None = None
    token_type: str = "bearer"
    refresh_token: str | None = None
    id_token: str | None = None
    created_at: PositiveInt = int(datetime.now(tz=timezone.utc).timestamp())
    expires_at: PositiveInt | None = None
