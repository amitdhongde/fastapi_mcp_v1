""" Import the required modules """
from typing import Any
from fastapi import APIRouter, Depends, Request

# Import middlewares and dependencies
from modules.base.fastapi.dependencies.authentication import AuthGuard

# Include the project controllers
from ..controllers.lookup_controller import LookupController as Controller

# Include the project models
from ..models.organization.request import (
    OrganizationCreateRequest,
    OrganizationUpdateRequest
)

# Create the module router
router = APIRouter(prefix="/lookup", tags=["LookUp"])

@router.get("/",
        dependencies=[Depends(AuthGuard)],
        name="get_lookups",
        operation_id="get_lookup_list"
    )
async def index(
        request: Request,
        auth: AuthGuard = Depends(AuthGuard)
    ) -> Any:
    """
    Get all lookup data.
    """
    current_user = auth.current_user()
    return await Controller().index(request, current_user)

@router.get("/{uid}",
        dependencies=[Depends(AuthGuard)],
        name="get_lookup",
        operation_id="get_lookup"
    )
async def show(
        uid: str,
        request: Request,
        auth: AuthGuard = Depends(AuthGuard)
    ) -> Any:
    """
    Get the lookup data with the given uid.
    """
    current_user = auth.current_user()
    return await Controller().show(uid, request, current_user)

@router.post("/",
        dependencies=[Depends(AuthGuard)],
        name="create_lookup",
        operation_id="create_lookup"
    )
async def create(
        payload: OrganizationCreateRequest,
        request: Request,
        auth: AuthGuard = Depends(AuthGuard)
    ) -> Any:
    """
    Create a new lookup with the given payload.
    """
    current_user = auth.current_user()
    return await Controller().create(
            payload, request,
            current_user
        )

@router.put("/{uid}",
        dependencies=[Depends(AuthGuard)],
        name="update_lookup",
        operation_id="update_lookup"
    )
async def update(
        uid: str,
        payload: OrganizationUpdateRequest,
        request: Request,
        auth: AuthGuard = Depends(AuthGuard)
    ) -> Any:
    """
    Update the lookup with the given uid and payload.
    """
    current_user = auth.current_user()
    return await Controller().update(
        uid, payload, request,
        current_user
    )

@router.delete("/{uid}",
        dependencies=[Depends(AuthGuard)],
        name="delete_lookup",
        operation_id="delete_lookup"
    )
async def delete(
        uid: str,
        request: Request,
        auth: AuthGuard = Depends(AuthGuard)
    ) -> Any:
    """
    Delete the lookup with the given uid.
    """
    current_user = auth.current_user()
    return await Controller().delete(
        uid, request,
        current_user
    )
