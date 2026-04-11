""" Import the required modules """
from typing import Annotated, Any

from fastmcp import FastMCP, Context
from fastmcp.dependencies import CurrentRequest, Depends
from starlette.requests import Request

# Include the project controllers
# from modules.base.fastapi.dependencies.common import common_parameters
from modules.note.controllers import NoteController as Controller

# Include the project models
from modules.base.models.auth import AuthClaim
from modules.note.models import (
        NoteCreateRequest,
        NoteUpdateRequest
    )

mcp = FastMCP()

@mcp.tool(
    name="get_a_notes_list_for_a_user",
    description="Get a list of notes for the authenticated user.",
    tags={"note", "get", "list"}
)
async def get_notes_list(
        request: Request = CurrentRequest(),
        limit: int = 10
    ) -> Any:
    """
    Get all note data.
    """
    claim:AuthClaim = request.state.claim
    return await Controller().index({"limit": limit}, request, claim)

# @mcp.tool(
#     name="get_a_note_with_a_given_uid",
#     description="Get a note with the given uid.",
#     tags={"note", "get"}
# )
# async def get_note(
#         uid: str, request: Request = CurrentRequest()
#     ) -> Any:
#     current_user = {"id":1, "name":"test", "email":"amit@bond.ai"}
#     return await Controller().show(uid, request, current_user)

# @mcp.tool(
#     name="create_a_note_with_any_text_content_and_title",
#     description="Create a new note with the given title and content.",
#     tags={"note", "create"}
# )
# async def create_note(
#         payload: NoteCreateRequest,
#         request: Request = CurrentRequest(),
#         controller: Controller = Depends()
#     ) -> Any:
#     """
#     Create a new note with the given payload.
#     """
#     current_user = {"id":1, "name":"test", "email":"amit@bond.ai"}
#     return await controller.create(
#             payload, request,
#             current_user
#         )

# @mcp.tool(
#     name="update_a_note_with_a_given_uid",
#     description="Update a note with the given uid and new title and content.",
#     tags={"note", "update"}
# )
# async def update_note(uid: str, title: str, content: str, request: Request, controller: Controller = Depends()) -> Any:
#     update_request = NoteUpdateRequest(title=title, content=content)
#     current_user = auth.current_user()
#     return await controller.update(uid, update_request, request, current_user)

# @mcp.tool(
#     name="delete_a_note_with_a_given_uid",
#     description="Delete a note with the given uid.",
#     tags={"note", "delete"}
# )
# async def delete_note(uid: str, request: Request, controller: Controller = Depends()) -> Any:
#     return await controller.delete(uid, request)
