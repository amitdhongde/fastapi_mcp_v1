""" Import the required modules """
from typing import Any
from fastapi import APIRouter, Depends, Request

# Import middlewares and dependencies
from modules.base.fastapi.dependencies.authentication import AuthGaurd

# Include the project controllers
from ..controllers import NoteController as Controller

# Include the project models
from ..models import (
    NoteCreateRequest,
    NoteUpdateRequest
)

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.get("/",
        dependencies=[Depends(AuthGaurd)],
        name="get_notes",
        operation_id="get_note_list"
    )
async def index(
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Get all lookup data.
    """
    current_user = auth.current_user()
    return await Controller().index(request, current_user)

@router.get("/{uid}",
        dependencies=[Depends(AuthGaurd)],
        name="get_note",
        operation_id="get_note"
    )
async def show(
        uid: str,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Get the note data with the given uid.
    """
    current_user = auth.current_user()
    return await Controller().show(uid, request, current_user)

@router.post("/",
        dependencies=[Depends(AuthGaurd)],
        name="create_note",
        operation_id="create_note"
    )
async def create(
        payload: NoteCreateRequest,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Create a new note with the given payload.
    """
    current_user = auth.current_user()
    return await Controller().create(
            payload, request,
            current_user
        )

@router.put("/{uid}",
        dependencies=[Depends(AuthGaurd)],
        name="update_note",
        operation_id="update_note"
    )
async def update(
        uid: str,
        payload: NoteUpdateRequest,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Update the note with the given uid and payload.
    """
    current_user = auth.current_user()
    return await Controller().update(
        uid, payload, request,
        current_user
    )

@router.delete("/{uid}",
        dependencies=[Depends(AuthGaurd)],
        name="delete_note",
        operation_id="delete_note"
    )
async def delete(
        uid: str,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Delete the note with the given uid.
    """
    current_user = auth.current_user()
    return await Controller().delete(
        uid, request,
        current_user
    )
