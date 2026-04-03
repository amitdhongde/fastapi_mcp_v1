""" Import the required modules """
from typing import Annotated, Any
from fastapi import APIRouter, Depends, Request

# Import middlewares and dependencies
from modules.base.fastapi.dependencies import (
    common_parameters
)
from modules.base.fastapi.dependencies.authentication import AuthGuard

# Include the project controllers
from modules.core.controllers import (
    OrganizationController as Controller
)

# Include the project models
from ..models.organization.request import (
    OrganizationCreateRequest,
    OrganizationUpdateRequest
)

# Exception classes
from modules.base.exceptions import (
    InvalidTokenException
)

# Create the module router
router = APIRouter(prefix="/organization", tags=["Organization"])

@router.get("/",
        dependencies=[
            Depends(AuthGuard),
            Depends(common_parameters)
        ],
        name="get_organizations",
        operation_id="get_organization_list"
    )
async def index(
        commons: Annotated[dict, Depends(common_parameters)],
        request: Request,
        auth: AuthGuard = Depends(AuthGuard)
    ) -> Any:
    """
    Get all organizations.
    """
    #current_user = auth.current_user()
    access_token: str = auth.valid_token()
    if not access_token:
        raise InvalidTokenException()

    current_user = {"id":1, "name":"test", "email":"amit@bond.ai"}
    return await Controller().index(commons, request, current_user)

@router.get("/{uid}",
        dependencies=[Depends(AuthGuard)],
        name="get_organization"
    )
async def show(
        uid: str,
        request: Request,
        auth: AuthGuard = Depends(AuthGuard)
    ) -> Any:
    """
    Get the organization with the given uid.
    """
    #current_user = auth.current_user()
    access_token: str = auth.valid_token()
    if not access_token:
        raise

    current_user = {"id":1, "name":"test", "email":"amit@bond.ai"}
    return await Controller().show(uid, request, current_user)

@router.post("/",
        dependencies=[Depends(AuthGuard)],
        name="create_organization"
    )
async def create(
        payload: OrganizationCreateRequest,
        request: Request,
        auth: AuthGuard = Depends(AuthGuard)
    ) -> Any:
    """
    Create a new organization with the given payload.
    """
    current_user = auth.current_user()
    return await Controller().create(
            payload, request,
            current_user
        )

@router.put("/{uid}",
        dependencies=[Depends(AuthGuard)],
        name="update_organization"
    )
async def update(
        uid: str,
        payload: OrganizationUpdateRequest,
        request: Request,
        auth: AuthGuard = Depends(AuthGuard)
    ) -> Any:
    """
    Update the organization with the given uid and payload.
    """
    current_user = auth.current_user()
    return await Controller().update(
        uid, payload, request,
        current_user
    )

@router.delete("/{uid}",
        dependencies=[Depends(AuthGuard)],
        name="delete_organization"
    )
async def delete(
        uid: str,
        request: Request,
        auth: AuthGuard = Depends(AuthGuard)
    ) -> Any:
    """
    Delete the organization with the given uid and payload.
    """
    current_user = auth.current_user()
    return await Controller().delete(
        uid, request,
        current_user
    )
