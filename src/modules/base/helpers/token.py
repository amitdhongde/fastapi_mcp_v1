import jwt
from datetime import datetime, timedelta, timezone
from modules.base.config import config
from modules.base.models.auth import AccessToken

class DecodeTokenException(Exception):
    code = 400
    error_code = "TOKEN__DECODE_ERROR"
    message = "token decode error"

class ExpiredTokenException(Exception):
    code = 400
    error_code = "TOKEN__EXPIRE_TOKEN"
    message = "expired token"

class TokenHelper:
    @staticmethod
    def encode(
            payload: dict, subject: str|None=None,
            expire_period: int = 3600
        ) -> AccessToken:
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
        except jwt.exceptions.DecodeError as exc:
            raise DecodeTokenException from exc
        except jwt.exceptions.ExpiredSignatureError as exc:
            raise ExpiredTokenException from exc

    @staticmethod
    def decode_expired_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                config.JWT_ALGORITHM,
                options={"verify_exp": False},
            )
        except jwt.exceptions.DecodeError as exc:
            raise DecodeTokenException from exc
