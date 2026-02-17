""" Import the required modules """
from server.api import start_api_server
from server.mcp import start_mcp_server

if __name__ == "__main__":
    start_api_server()
    # start_mcp_server()
