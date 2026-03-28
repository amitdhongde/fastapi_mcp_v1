""" Import the required modules """
from datetime import datetime, timedelta, timezone
import jwt

# Import the required modules from the project
from modules.base.config import config
from modules.base.models.auth import AccessToken
from modules.base.exceptions import InvalidTokenException

class TokenHelper:
    @staticmethod
    def encode(
            payload: dict, subject: str|None=None,
            expire_period: int = 3600
        ) -> AccessToken:
        try:
            # Set the expiration time
            expires_at: datetime = datetime.now(tz=timezone.utc) + timedelta(seconds=expire_period)

            # Set the payload
            token: AccessToken = AccessToken()
            token.access_token = jwt.encode(
                payload={
                    **payload,
                    "exp": expires_at,                      # expiration time
                    "iat": datetime.now(tz=timezone.utc),   # issued at
                    "nbf": datetime.now(tz=timezone.utc),   # not before
                    "iss": config.JWT_ISSUER,               # issuer
                    "aud": config.JWT_AUDIENCE,             # audience
                    "sub": subject,                         # subject
                },
                key=config.JWT_SECRET_KEY,
                algorithm=config.JWT_ALGORITHM,
            )
            token.expires_at = int(expires_at.timestamp())
            return token
        except (jwt.exceptions.PyJWTError, Exception) as exc:
            raise InvalidTokenException(str(exc)) from exc

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                config.JWT_ALGORITHM,
                audience=config.JWT_AUDIENCE,
                issuer=config.JWT_ISSUER
            )
        except jwt.exceptions.ExpiredSignatureError as exc:
            raise InvalidTokenException(
                    'Token expired', 'error_code_expired_token'
                ) from exc
        except (jwt.exceptions.PyJWTError, Exception) as exc:
            raise InvalidTokenException(str(exc)) from exc

    @staticmethod
    def decode_expired_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                config.JWT_ALGORITHM,
                options={"verify_exp": False},
            )
        except (jwt.exceptions.PyJWTError, Exception) as exc:
            raise InvalidTokenException(str(exc)) from exc
