""" Import the required modules """
import logging
import uvicorn

from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

# Import the project configuration
from modules.base.config import config

# MCP Application
mcp_app = FastAPI(
    title=config.MCP_NAME,
    description=config.MCP_DESCRIPTION,
    version=config.MCP_VERSION,
    debug=config.DEBUG,
    docs_url=None if config.ENVIRONMENT == "production" else "/mcp/documentation",
    redoc_url=None if config.ENVIRONMENT == "production" else "/mcp/redocumentation",
)
mcp = FastApiMCP(
    mcp_app,
    name=config.MCP_NAME,
    description=config.MCP_DESCRIPTION,
    describe_full_response_schema=True,  # Describe the full response JSON-schema instead of just a response example
    describe_all_responses=True,  # Describe all the possible responses instead of just the success (2XX) response
)

# Mount the MCP application to the main FastAPI app
mcp.mount_http(
    mcp_app
)

# Add new endpoints after MCP server creation
@mcp_app.get("/sns", operation_id="get_message_qmh_sf_pb")
async def new_endpoint():
    return {"message": "RR5555SF343434343434"}

# Refresh the MCP server to include the new endpoint
mcp.setup_server()

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
