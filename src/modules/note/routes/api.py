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
from modules.note.controllers import NoteController as Controller

# Include the project models
from modules.base.models.response import JsonSuccessResponse
from modules.note.models import (
        NoteCreateRequest,
        NoteUpdateRequest
    )

router = APIRouter(prefix="/note", tags=["Notes"])

@router.get("/",
        dependencies=[
            Depends(get_auth_guard),
            Depends(common_parameters)
        ],
        name="get_notes",
        operation_id="get_note_list"
    )
@permissions("note_read")
async def index(
        commons: Annotated[dict, Depends(common_parameters)],
        guard: Annotated[AuthGuard, Depends(get_auth_guard)],
        request: Request,
        controller: Controller = Depends()
    ) -> JsonSuccessResponse:
    """
    Get all note data.
    """
    return await controller.index(commons, request, guard.get_claim())

@router.get("/{uid}",
        dependencies=[Depends(get_auth_guard)],
        name="get_note",
        operation_id="get_note"
    )
@permissions("note_read")
async def show(
        uid: str,
        request: Request,
        guard: Annotated[AuthGuard, Depends(get_auth_guard)],
        controller: Controller = Depends()
    ) -> JsonSuccessResponse:
    """
    Get the note data with the given UID.
    """
    return await controller.show(uid, request, guard.get_claim())

@router.post("/",
        dependencies=[Depends(get_auth_guard)],
        name="create_note",
        operation_id="create_note"
    )
@permissions("note_create")
async def create(
        payload: NoteCreateRequest,
        request: Request,
        guard: Annotated[AuthGuard, Depends(get_auth_guard)],
        controller: Controller = Depends()
    ) -> JsonSuccessResponse:
    """
    Create a new note with the given payload.
    """
    return await controller.create(
            payload, request,
            guard.get_claim()
        )

@router.put("/{uid}",
        dependencies=[Depends(get_auth_guard)],
        name="update_note",
        operation_id="update_note"
    )
@permissions("note_update")
async def update(
        uid: str,
        payload: NoteUpdateRequest,
        request: Request,
        guard: Annotated[AuthGuard, Depends(get_auth_guard)],
        controller: Controller = Depends()
    ) -> JsonSuccessResponse:
    """
    Update the note with the given UID and payload.
    """
    return await controller.update(
            uid, payload, request,
            guard.get_claim()
        )

@router.delete("/{uid}",
        dependencies=[Depends(get_auth_guard)],
        name="delete_note",
        operation_id="delete_note"
    )
@permissions("note_delete")
async def delete(
        uid: str,
        request: Request,
        guard: Annotated[AuthGuard, Depends(get_auth_guard)],
        controller: Controller = Depends()
    ) -> JsonSuccessResponse:
    """
    Delete the note with the given UID.
    """
    return await controller.delete(
            uid, request,
            guard.get_claim()
        )
