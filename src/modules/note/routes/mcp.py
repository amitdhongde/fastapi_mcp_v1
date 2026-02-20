from typing import Any

from fastmcp.tools import tool
from starlette.requests import Request

# Include the project controllers
from ..controllers import NoteController as Controller

@tool(
    name="create_note",
    description="Create a new note with the given title and content.",
    tags=["note", "create"]
)
async def create_note(content: str, title: str, request: Request) -> Any:
    return await Controller().create(
            title, content, request,
        )
