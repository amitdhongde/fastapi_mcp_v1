""" Import the required modules """
from typing import Annotated, Any
from fastapi import APIRouter, Depends, Request

# Import middlewares and dependencies
from modules.base.fastapi.dependencies import (
        common_parameters
    )

# Import middlewares and dependencies
from modules.base.fastapi.dependencies.authentication import AuthGaurd

# Include the project controllers
from ..controllers import NoteController as Controller

# Include the project models
from ..models import (
        NoteCreateRequest,
        NoteUpdateRequest
    )

# Include the project exceptions
from modules.base.exceptions import (
        InvalidTokenException
    )

router = APIRouter(prefix="/note", tags=["Notes"])

@router.get("/",
        dependencies=[
            Depends(AuthGaurd),
            Depends(common_parameters)
        ],
        name="get_notes",
        operation_id="get_note_list"
    )
async def index(
        commons: Annotated[dict, Depends(common_parameters)],
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Get all note data.
    """
    access_token: str = auth.valid_token()
    if not access_token:
        raise InvalidTokenException()

    return await Controller().index(commons, request, auth.get_user())

@router.get("/{hash}",
        dependencies=[Depends(AuthGaurd)],
        name="get_note",
        operation_id="get_note"
    )
async def show(
        hash: str,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Get the note data with the given hash.
    """
    #current_user = auth.current_user()
    access_token: str = auth.valid_token()
    if not access_token:
        raise InvalidTokenException()

    current_user = {"id":1, "name":"test", "email":"amit@bond.ai"}
    return await Controller().show(hash, request, current_user)

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
    #current_user = auth.current_user()
    access_token: str = auth.valid_token()
    if not access_token:
        raise InvalidTokenException()

    current_user = {"id":1, "name":"test", "email":"amit@bond.ai"}

    return await Controller().create(
            payload, request,
            current_user
        )

@router.put("/{hash}",
        dependencies=[Depends(AuthGaurd)],
        name="update_note",
        operation_id="update_note"
    )
async def update(
        hash: str,
        payload: NoteUpdateRequest,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Update the note with the given hash and payload.
    """
    current_user = auth.current_user()
    return await Controller().update(
        hash, payload, request,
        current_user
    )

@router.delete("/{hash}",
        dependencies=[Depends(AuthGaurd)],
        name="delete_note",
        operation_id="delete_note"
    )
async def delete(
        hash: str,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Delete the note with the given hash.
    """
    current_user = auth.current_user()
    return await Controller().delete(
        hash, request,
        current_user
    )
