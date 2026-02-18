## Installation
- Create virtual environment at project level with folder name .venv
```bash
python -m venv .venv
poetry install
```
- Synchronize Poetry
```bash
poetry sync
```

# Start API Server
- Open new CMD Terminal
- Run below cmd
```bash
poetry run api_app
```

## Start MCP Server
- Open new CMD Terminal
- Activate the virtual environemnt
- Run below cmd
```bash 
poetry run mcp_app
```