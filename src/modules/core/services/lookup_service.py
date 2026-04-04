""" Import the required modules """
import logging
from typing import List
from fastapi import Request
from pydantic import TypeAdapter, BaseModel

# Include the project models
from modules.core.enums import LookupMaster
from modules.core.models.organization.request import (
    OrganizationCreateRequest,
    OrganizationUpdateRequest
)
from modules.core.models.lookup import (
        Lookup,
        LookupMinor,
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
            self, payload: OrganizationCreateRequest, ip_address: str,
            current_user: BaseModel) -> LookupFullResponse:
        """ Create a new object """
        try :
            # Validate the credentials
            model: LookupFullResponse = await self.repository.save(
                payload, ip_address, current_user
            )
            if not model:
                raise EntityNotSavedException(
                    message="Unable to create the lookup"
                )

            return model
        except Exception as e:
            raise e

    async def update(
            self, uid: str, payload: OrganizationUpdateRequest,
            ip_address: str, current_user: BaseModel) -> LookupFullResponse:
        """ Update the model """
        try:
            # Get the claim from storage
            model: LookupFullResponse = await self.repository.update_by_hash(
                uid, payload, ip_address, current_user
            )
            if not model:
                raise EntityNotSavedException(
                    message="Unable to update the lookup"
                )

            return model
        except Exception as e:
            raise e

    async def delete(
            self, uid: str, ip_address: str,
            current_user: BaseModel) -> LookupFullResponse:
        """ Delete the model """
        try:
            model: LookupFullResponse = await self.repository.delete_by_hash(
                uid, ip_address, current_user
            )
            if not model:
                raise EntityNotFoundException(
                    message="Unable to delete the lookup"
                )

            return model
        except Exception as e:
            raise e

    async def list(
            self,
            commons: dict,
            request: Request,
            ip_address: str
        ) -> List[LookupMinorResponse]:
        """ List all the objects """
        try:
            # Validate the payload
            response = await self.repository.get_all(
                    skip=commons.get("skip", 0),
                    limit=commons.get("limit", 100),
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
            ip_address: str
        ) -> LookupFullResponse:
        """ Get the object """
        try:
            # Validate the payload
            response = await self.repository.get_by_hash(uid)
            if not response:
                raise EntityNotFoundException(
                    message="Unable to get the lookup from IP address = " + ip_address
                )

            # Validate the response
            model: LookupFullResponse = \
                TypeAdapter(LookupFullResponse).validate_python(response)

            return model
        except Exception as e:
            raise e
        
    async def get_by_type(
            self,
            type: LookupMaster
        ) -> List[LookupFullResponse]:
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
            key: str
        ) -> LookupFullResponse:
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