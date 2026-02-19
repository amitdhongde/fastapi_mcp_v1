""" Import the required modules """
from typing import Any
from fastapi import APIRouter, Depends, Request

# Import middlewares and dependencies
from modules.base.fastapi.dependencies.authentication import AuthGaurd

# Include the project controllers
from ..controllers import DocumentController as Controller

# Include the project models
from ..models import (
    DocumentCreateRequest,
    DocumentUpdateRequest
)

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.get("/",
        dependencies=[Depends(AuthGaurd)],
        name="get_documents",
        operation_id="get_document_list"
    )
async def index(
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Get all documents.
    """
    current_user = auth.current_user()
    return await Controller().index(request, current_user)

@router.get("/{uid}",
        dependencies=[Depends(AuthGaurd)],
        name="get_document",
        operation_id="get_document"
    )
async def show(
        uid: str,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Get the document data with the given uid.
    """
    current_user = auth.current_user()
    return await Controller().show(uid, request, current_user)

@router.post("/",
        dependencies=[Depends(AuthGaurd)],
        name="create_document",
        operation_id="create_document"
    )
async def create(
        payload: DocumentCreateRequest,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Create a new document with the given payload.
    """
    current_user = auth.current_user()
    return await Controller().create(
            payload, request,
            current_user
        )

@router.put("/{uid}",
        dependencies=[Depends(AuthGaurd)],
        name="update_document",
        operation_id="update_document"
    )
async def update(
        uid: str,
        payload: DocumentUpdateRequest,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Update the document with the given uid and payload.
    """
    current_user = auth.current_user()
    return await Controller().update(
        uid, payload, request,
        current_user
    )

@router.delete("/{uid}",
        dependencies=[Depends(AuthGaurd)],
        name="delete_document",
        operation_id="delete_document"
    )
async def delete(
        uid: str,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Delete the document with the given uid.
    """
    current_user = auth.current_user()
    return await Controller().delete(
        uid, request,
        current_user
    )
