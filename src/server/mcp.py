""" Import the required modules """
import logging
import uvicorn

from fastapi import FastAPI
from fastmcp import FastMCP

# Import the project configuration
from modules.base.config import config

# Import the other MCP tools
from modules.note.routes import note_mcp

# MCP Server setup
mcp = FastMCP(
    name=config.MCP_NAME,
    version=config.MCP_VERSION,
    instructions=config.MCP_DESCRIPTION
)

# Mount other MCP tools
mcp.mount(note_mcp)


# Add new tools to the MCP server
@mcp.tool
def greeting(name: str) -> dict:
    """Greet, send message, text a user by name."""
    if name.casefold() in [item.casefold() for item in config.SNS_NAMES]:
        return {"message": f"Hey {name}, RR5555SF343434!"}
    else:
        return {"message": f"Hello, {name}! Wishing you a great day from aQveir!"}
    
@mcp.tool
def add_numbers(a: int, b: int) -> dict:
    """Add two numbers and return the result."""
    result = a + b
    return {"result": result}

@mcp.tool
def multiply_numbers(a: int, b: int) -> dict:
    """Multiply two numbers and return the result."""
    result = a * b
    return {"result": result}

@mcp.tool
def divide_numbers(a: int, b: int) -> dict:
    """Divide two numbers and return the result."""
    if b == 0:
        return {"error": "Cannot divide by zero."}
    result = a / b
    return {"result": result}

@mcp.tool
def subtract_numbers(a: int, b: int) -> dict:
    """Subtract two numbers and return the result."""
    result = a - b
    return {"result": result}

# Create the MCP ASGI app with path="/"
mcp_app = mcp.http_app(path="/")

# Create FastAPI app with MCP lifespan (required for session management)
api = FastAPI(lifespan=mcp_app.lifespan)

# Mount MCP at /mcp
api.mount("/mcp", mcp_app)

# Start the MCP server
def start_mcp_server():
    """ Start the Uvicorn server """
    logging.info('********** MCP Server **********')
    uvicorn.run(
        app="server.mcp:api",
        host=config.MCP_HOST,
        port=config.MCP_PORT,
        log_level="debug" if config.ENVIRONMENT != "production" else "info"
    )

# Run the MCP server if this file is executed directly
if __name__ == "__main__":
    start_mcp_server()
