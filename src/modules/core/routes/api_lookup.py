""" Import the required modules """
from typing import Annotated, Any
from fastapi import APIRouter, Depends, Request

# Import middlewares and dependencies
from modules.base.fastapi.decorations import permissions
from modules.base.fastapi.dependencies import (
        common_parameters
    )
from modules.base.fastapi.dependencies.authentication import (
        AuthGuard,
        get_auth_guard
    )

# Include the project controllers
from modules.core.controllers import LookupController as Controller

# Include the project models
from modules.base.models.response import JsonSuccessResponse
from modules.core.models.lookup import (
        LookupCreateRequest,
        LookupUpdateRequest
    )

# Create the module router
router = APIRouter(prefix="/lookup", tags=["LookUp"])

@router.get("/",
        dependencies=[
            Depends(get_auth_guard),
            Depends(common_parameters)
        ],
        name="get_lookups",
        operation_id="get_lookup_list"
    )
@permissions("lookup_read")
async def index(
        commons: Annotated[dict, Depends(common_parameters)],
        guard: Annotated[AuthGuard, Depends(get_auth_guard)],
        request: Request,
        controller: Controller = Depends()
    ) -> JsonSuccessResponse:
    """
    Get all lookup data.
    """
    return await controller.index(commons, request, guard)

@router.get("/{uid}",
        dependencies=[Depends(AuthGuard)],
        name="get_lookup",
        operation_id="get_lookup"
    )
@permissions("lookup_read")
async def show(
        uid: str,
        request: Request,
        guard: Annotated[AuthGuard, Depends(get_auth_guard)],
        controller: Controller = Depends()
    ) -> JsonSuccessResponse:
    """
    Get the lookup data with the given uid.
    """
    return await controller.show(uid, request, guard)

@router.post("/",
        dependencies=[Depends(get_auth_guard)],
        name="create_lookup",
        operation_id="create_lookup"
    )
@permissions("lookup_create")
async def create(
        payload: LookupCreateRequest,
        request: Request,
        guard: Annotated[AuthGuard, Depends(get_auth_guard)],
        controller: Controller = Depends()
    ) -> JsonSuccessResponse:
    """
    Create a new lookup with the given payload.
    """
    return await controller.create(
            payload, request,
            guard
        )

@router.put("/{uid}",
        dependencies=[Depends(get_auth_guard)],
        name="update_lookup",
        operation_id="update_lookup"
    )
@permissions("lookup_update")
async def update(
        uid: str,
        payload: LookupUpdateRequest,
        request: Request,
        guard: Annotated[AuthGuard, Depends(get_auth_guard)],
        controller: Controller = Depends()
    ) -> JsonSuccessResponse:
    """
    Update the lookup with the given uid and payload.
    """
    return await controller.update(
            uid, payload, request,
            guard
        )

@router.delete("/{uid}",
        dependencies=[Depends(get_auth_guard)],
        name="delete_lookup",
        operation_id="delete_lookup"
    )
@permissions("lookup_delete")
async def delete(
        uid: str,
        request: Request,
        guard: Annotated[AuthGuard, Depends(get_auth_guard)],
        controller: Controller = Depends()
    ) -> JsonSuccessResponse:
    """
    Delete the lookup with the given uid.
    """
    return await controller.delete(
            uid, request,
            guard
        )
