from typing import Any

from fastmcp import FastMCP
from starlette.requests import Request

# Include the project controllers
from ..controllers import NoteController as Controller

# Include the project models
from ..models import (
    NoteCreateRequest,
    NoteUpdateRequest
)

mcp = FastMCP()

@mcp.tool(
    name="get a notes list for a user",
    description="Get a list of notes for the authenticated user.",
    tags=["note", "get", "list"]
)
async def get_notes_list(request: Request) -> Any:
    return await Controller().list(request)

@mcp.tool(
    name="get a note with a given uid",
    description="Get a note with the given uid.",
    tags=["note", "get"]
)
async def get_note(uid: str, request: Request) -> Any:
    return await Controller().show(uid, request)

@mcp.tool(
    name="create a note with any text content and title",
    description="Create a new note with the given title and content.",
    tags=["note", "create"]
)
async def create_note(content: str, title: str, request: Request) -> Any:
    create_request = NoteCreateRequest(title=title, content=content)
    current_user = auth.current_user()
    return await Controller().create(create_request, request, current_user)

@mcp.tool(
    name="update a note with a given uid",
    description="Update a note with the given uid and new title and content.",
    tags=["note", "update"]
)
async def update_note(uid: str, title: str, content: str, request: Request) -> Any:
    update_request = NoteUpdateRequest(title=title, content=content)
    current_user = auth.current_user()
    return await Controller().update(uid, update_request, request, current_user)

@mcp.tool(
    name="delete a note with a given uid",
    description="Delete a note with the given uid.",
    tags=["note", "delete"]
)
async def delete_note(uid: str, request: Request) -> Any:
    return await Controller().delete(uid, request)
