""" Import the required modules """
import logging
from typing import List
from starlette.requests import Request
from pydantic import TypeAdapter

# Include the project models
from modules.core.enums import LookupMaster
from modules.base.fastapi.dependencies.authentication import (
        AuthGuard
    )
from modules.core.models.lookup import (
        LookupFullResponse,
        LookupMinorResponse
    )

# include the project services
from modules.base.services.base import BaseService

# Include the module repositories
from modules.core.repositories import LookupRepository

# Include the module exceptions
from modules.base.exceptions.base import (
        EntityNotFoundException,
        EntityNotSavedException
    )

# Initialize the logger
logger = logging.getLogger(__name__)

class LookupService(BaseService):
    """ LookupService class to handle lookup related operations. """
    def __init__(self):
        self.repository = LookupRepository()
        super().__init__(self.repository)

    async def create(
            self, payload: dict,
            request: Request,
            guard: AuthGuard) -> LookupFullResponse:
        """ Create a new object """
        try :
            # Add the organization id to the payload
            payload["organization_id"] = guard.get_token_value('org_id')

            # Validate the credentials
            response = await self.repository.create(
                    payload,
                    guard.get_token_value('user_id')
                )
            if not response:
                raise EntityNotSavedException(
                    message="Unable to create the lookup"
                )

            # Validate the response
            model: LookupFullResponse = \
                TypeAdapter(LookupFullResponse).validate_python(response)

            return model
        except Exception as e:
            raise e

    async def update(
            self, uid: str,
            payload: dict,
            request: Request,
            guard: AuthGuard) -> LookupFullResponse:
        """ Update the model """
        try:
            # Build the conditions for the query
            conditions = {}
            if guard is not None:
                conditions["organization_id"] = guard.get_token_value('org_id')

            # Get the claim from storage
            response = await self.repository.update_by_uid(
                    uid, payload,
                    conditions=conditions,
                    updated_by=guard.get_token_value('user_id')
                )
            if not response:
                raise EntityNotSavedException(
                    message="Unable to update the lookup"
                )

            # Validate the response
            model: LookupFullResponse = \
                TypeAdapter(LookupFullResponse).validate_python(response)

            return model
        except Exception as e:
            raise e

    async def delete(
            self, uid: str,
            request: Request,
            guard: AuthGuard) -> LookupFullResponse:
        """ Delete the model """
        try:
            # Build the conditions for the query
            conditions = {}
            if guard is not None:
                conditions["organization_id"] = guard.get_token_value('org_id')

            response = await self.repository.delete_by_uid(
                    uid,
                    conditions=conditions,
                    deleted_by=guard.get_token_value('user_id')
                )
            if not response:
                raise EntityNotFoundException(
                    message="Unable to delete the lookup"
                )

            # Validate the response
            model: LookupFullResponse = \
                TypeAdapter(LookupFullResponse).validate_python(response)

            return model
        except Exception as e:
            raise e

    async def list(
            self,
            commons: dict,
            request: Request,
            guard: AuthGuard) -> List[LookupMinorResponse]:
        """ List all the objects """
        try:
            # Create conditions for the query
            conditions = {}
            if guard is not None:
                conditions["or_"] = [
                    ("organization_id", "==", guard.get_token_value('org_id')),
                    ("organization_id", "==", "0")
                ]

            # Conditions for the query
            if commons.get("q") is not None:
                _query: list[str] = commons.get("q", {})
                for data in _query:
                    field, value = data.split("=")
                    conditions[field] = value

            # Validate the payload
            response = await self.repository.get_all(
                    skip=commons.get("skip", 0),
                    limit=commons.get("limit", 100),
                    conditions=conditions
                )
            if not response:
                raise EntityNotFoundException(
                    message="Unable to get the lookups from IP address."
                )

            # Validate the response
            models: List[LookupMinorResponse] = \
                TypeAdapter(List[LookupMinorResponse]).validate_python(response)

            return models
        except Exception as e:
            raise e

    async def get(
            self,
            uid: str,
            request: Request,
            guard: AuthGuard) -> LookupFullResponse:
        """ Get the object """
        try:
            # Create conditions for the query
            conditions = {}
            if guard is not None:
                conditions["organization_id"] = guard.get_token_value('org_id')

            # Validate the payload
            response = await self.repository.get_by_hash(uid, conditions=conditions)
            if not response:
                raise EntityNotFoundException(
                    message="Unable to get the lookup"
                )

            # Validate the response
            model: LookupFullResponse = \
                TypeAdapter(LookupFullResponse).validate_python(response)

            return model
        except Exception as e:
            raise e

    async def get_by_type(
            self,
            type: LookupMaster) -> List[LookupFullResponse]:
        """ Get the lookup object by type
            param type: LookupMaster - The type of the lookup to be fetched
            returns: List[LookupFullResponse] - The list of lookups of the given type
        """
        try:
            # Validate the payload
            response = await self.repository.get_by(
                    field='lookup_type',
                    value=str(type.value),
                    conditions={"is_active": True}
                )

            if not response:
                raise EntityNotFoundException(
                    message="Unable to get the lookup"
                )

            # Validate the response
            models: List[LookupFullResponse] = \
                TypeAdapter(List[LookupFullResponse]).validate_python(response)

            return models
        except Exception as e:
            raise e

    async def get_by_key(
            self,
            key: str) -> LookupFullResponse:
        """ Get the lookup object by key
            param key: str - The key of the lookup to be fetched
            returns: LookupFullResponse - The lookup object of the given key
        """
        try:
            # Validate the payload
            response = await self.repository.get_by(
                    field='lookup_key',
                    value=key,
                    conditions={"is_active": True}
                )

            if not response:
                raise EntityNotFoundException(
                    message="Unable to get the lookup"
                )

            # Validate the response
            model: LookupFullResponse = \
                TypeAdapter(LookupFullResponse).validate_python(response)

            return model
        except Exception as e:
            raise e
