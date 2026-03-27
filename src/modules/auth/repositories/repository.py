""" Import the required modules """
import logging
from typing import Any, Set
from xml.parsers.expat import model
from pydantic import TypeAdapter, BaseModel
from modules.base.repository import BaseRepository

# Import the schema and model classes
from modules.auth.schemas import AuthSchema
from modules.auth.models import AuthFullResponse

logger = logging.getLogger(__name__)

class AuthRepository(BaseRepository[AuthSchema]):
    """
    This class to handle object related database operations.

    This class provides methods to perform CRUD operations on the database.
    It uses SQLAlchemy to interact with the database.
    """
    def __init__(self, model = AuthSchema):
        self.model = model
        super().__init__(model)

    async def authenticate_user(self, payload: dict,
            ip_address: str|None = None) -> AuthFullResponse|None:
        """ Authenticate the user with the given credentials and IP address."""
        try:
            # build the credentials query
            credentials: dict[str, Any] = {
                "username": payload.get("username"),
                "password": payload.get("code"),
                "is_active": True
            }

            # Get the user from the database
            response_list: list[AuthSchema] = await self.get_by_fields(credentials)

            if not response_list:
                return None
            else:
                authenticated_user: AuthSchema = response_list[0]

                # Validate the response
                return TypeAdapter(AuthFullResponse).validate_python(authenticated_user)
        except Exception as e:
            raise e

    async def show(self, hash: str):
        return f'UserRepository show {hash}'

    async def create(self):
        return 'UserRepository create'

    async def update(self, hash: str):
        return f'UserRepository update {hash}'

    async def delete(self, hash: str):
        return f'UserRepository delete {hash}'
