""" Import the required modules """
import logging
from typing import List
from fastapi import Request
from pydantic import TypeAdapter, BaseModel

# Include the project models
from modules.user.models import (
    UserCreateRequest,
    UserUpdateRequest
)
from modules.user.models import (User, UserMinor, UserFullResponse)

# include the project services
from modules.base.services import BaseService

# Include the module repositories
from modules.user.repositories import UserRepository

# Include the module exceptions
from modules.base.exceptions import (
    EntityNotFoundException,
    EntityNotSavedException
)

# Include the module events
from ..events import (
    UserCreatedEvent,
    UserUpdatedEvent,
    UserDeletedEvent
)

# Initialize the logger
logger = logging.getLogger(__name__)

class UserService(BaseService):
    """ Service class to handle all user related operations. """
    def __init__(self):
        self.repository = UserRepository()
        super().__init__(self.repository)

    async def create(
            self, payload: dict, ip_address: str,
            current_user: BaseModel) -> User:
        """ Create a new object """
        try :
            print(payload)
            # add the user id to the payload
            payload["organization_id"] = 1

            # Validate the credentials
            response = await self.repository.create(
                payload
            )

            if not response:
                raise EntityNotSavedException(
                    message="Unable to create the user"
                )

            # Validate the response
            model: User = TypeAdapter(User).validate_python(response)

            # Raise event on successful creation
            UserCreatedEvent().raise_event(model)

            return model
        except Exception as e:
            raise e

    async def update(
            self, uid: str, payload: UserUpdateRequest,
            ip_address: str, current_user: BaseModel) -> User:
        """ Update the model """
        try:
            # Get the claim from storage
            response = await self.repository.update_by_hash(
                uid, payload, ip_address, current_user
            )
            if not response:
                raise EntityNotSavedException(
                    message="Unable to update the user"
                )

            # Validate the response
            model: User = TypeAdapter(User).validate_python(response)

            # Raise event on successful update
            UserUpdatedEvent().raise_event(model)

            return model
        except Exception as e:
            raise e

    async def delete(
            self, uid: str, ip_address: str,
            current_user: BaseModel) -> User:
        """ Delete the model """
        try:
            response = await self.repository.delete_by_hash(
                uid, ip_address, current_user
            )
            if not response:
                raise EntityNotFoundException(
                    message="Unable to delete the user"
                )

            # Validate the response
            model: User = TypeAdapter(User).validate_python(response)

            # Raise event on successful deletion
            UserDeletedEvent().raise_event(model)            

            return model
        except Exception as e:
            raise e

    async def list(
            self,
            commons: dict,
            request: Request,
            ip_address: str
        ) -> List[User]:
        """ List all the objects """
        try:
            # Validate the payload
            response = await self.repository.get_all(
                skip=commons.get("skip", 0),
                limit=commons.get("limit", 100),
            )
            logger.debug(f"User count: {len(response)}")
            if not response:
                raise EntityNotFoundException(
                    message="Unable to get the users from IP address."
                )
            
            # Validate the response
            models: List[UserMinor] = TypeAdapter(List[UserMinor]).validate_python(response)

            return models
        except Exception as e:
            raise e

    async def get(
            self,
            uid: str,
            ip_address: str
        ) -> User:
        """ Get the object """
        try:
            # Validate the payload
            response = await self.repository.get_by_hash(uid)
            if not response:
                raise EntityNotFoundException(
                    message="Unable to get the user from IP address = " + ip_address
                )

            # Validate the response
            model: UserFullResponse = TypeAdapter(UserFullResponse).validate_python(response)

            return model
        except Exception as e:
            raise e
