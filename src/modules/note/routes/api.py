""" Import the required modules """
from typing import Annotated, Any
from fastapi import APIRouter, Depends, Request

# Import middlewares and dependencies
from modules.base.fastapi.dependencies import (
        common_parameters
    )

# Import middlewares and dependencies
from modules.base.fastapi.dependencies.authentication import (
        AuthGaurd
    )
from modules.base.models.response import JsonSuccessResponse
from modules.base.fastapi.decorations import permissions

# Include the project controllers
from modules.note.controllers import NoteController as Controller

# Include the project models
from modules.note.models import (
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
        operation_id="get_note_list",
        status_code=200
    )
@permissions("note_read")
async def index(
        commons: Annotated[dict, Depends(common_parameters)],
        request: Request,
        auth: Annotated[AuthGaurd, Depends(AuthGaurd)],
        controller: Controller = Depends()
    ) -> JsonSuccessResponse:
    """
    Get all note data.
    """
    return await controller.index(commons, request, auth.get_token_data())

@router.get("/{uid}",
        dependencies=[Depends(AuthGaurd)],
        name="get_note",
        operation_id="get_note"
    )
@permissions("note_read")
async def show(
        uid: str,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd),
        controller: Controller = Depends()
    ) -> Any:
    """
    Get the note data with the given UID.
    """
    #current_user = auth.current_user()
    access_token: str = auth.valid_token()
    if not access_token:
        raise InvalidTokenException()

    current_user = {"id":1, "name":"test", "email":"amit@bond.ai"}
    return await controller.show(uid, request, current_user)

@router.post("/",
        dependencies=[Depends(AuthGaurd)],
        name="create_note",
        operation_id="create_note"
    )
@permissions("note_create")
async def create(
        payload: NoteCreateRequest,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd),
        controller: Controller = Depends()
    ) -> Any:
    """
    Create a new note with the given payload.
    """
    #current_user = auth.current_user()
    access_token: str = auth.valid_token()
    if not access_token:
        raise InvalidTokenException()

    current_user = {"id":1, "name":"test", "email":"amit@bond.ai"}

    return await controller.create(
            payload, request,
            current_user
        )

@router.put("/{uid}",
        dependencies=[Depends(AuthGaurd)],
        name="update_note",
        operation_id="update_note"
    )
@permissions("note_update")
async def update(
        uid: str,
        payload: NoteUpdateRequest,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd),
        controller: Controller = Depends()
    ) -> Any:
    """
    Update the note with the given UID and payload.
    """
    current_user = auth.current_user()
    return await controller.update(
        uid, payload, request,
        current_user
    )

@router.delete("/{uid}",
        dependencies=[Depends(AuthGaurd)],
        name="delete_note",
        operation_id="delete_note"
    )
@permissions("note_delete")
async def delete(
        uid: str,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd),
        controller: Controller = Depends()
    ) -> Any:
    """
    Delete the note with the given UID.
    """
    current_user = auth.current_user()
    return await controller.delete(
        uid, request,
        current_user
    )
