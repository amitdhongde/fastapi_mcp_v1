""" Import the required modules """
import logging
import uvicorn

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from fastmcp.server.lifespan import lifespan

# Import the project configuration
from modules.base.config import config

# Import the other MCP tools
from modules.note.routes import note_mcp

# Get root logger
# the __name__ resolve to "main" since we are at the root of the project.
# This will get the root logger since no logger in the configuration has
# this name.
logger = logging.getLogger(__name__)

# Add Routers
def init_routers(_mcp: FastMCP) -> None:
    """ Initialize the routers for the FastAPI app.

    This is used to add the routers to the application. This will
    make the routes available in the app.

    The include_router function takes the router as an argument and 
    adds the routes to the app.
    """
    _mcp.mount(note_mcp)

# Lifespan Event Handler
@lifespan
async def mcp_lifespan(_mcp: FastMCP):
    """Lifespan event handler for the FastAPI app.

    This function is called when the app starts and stops.
    It is used to set up and tear down resources that are needed
    for the app to run.
    """
    # Setup log event handlers
    # setup_log_event_handlers()
    try:
        # Starting the server
        logger.info("********** Starting the server **********")

        # Initialize routers
        init_routers(_mcp=_mcp)

        # Initilize Exception Handlers
        # init_handlers(_mcp=_mcp)

        yield
    finally:
        # Stopping the server
        logger.info("********** Stopping the server **********")

        # Cleanup log event handlers
        # cleanup_log_event_handlers()

        # Cleanup resources here if needed
        logger.info("********** Server Stopped **********")

# MCP Server setup
mcp = FastMCP(
    name=config.MCP_NAME,
    version=config.MCP_VERSION,
    instructions=config.MCP_DESCRIPTION,
    lifespan=mcp_lifespan
)

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

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

# Create the MCP ASGI app with the defined tools
mcp_app = mcp.http_app(path="/mcp")

# Start the MCP server
def start_mcp_server():
    """ Start the Uvicorn server """
    logging.info('********** MCP Server **********')
    uvicorn.run(
        app="server.mcp:mcp_app",
        host=config.MCP_HOST,
        port=config.MCP_PORT,
        log_level="debug" if config.ENVIRONMENT != "production" else "info"
    )

# Run the MCP server if this file is executed directly
if __name__ == "__main__":
    start_mcp_server()
