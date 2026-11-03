# MCP: Model Context Protocol Servers

Building MCP servers in Python that give LLM clients (Claude Code, Claude Desktop, VS Code Copilot) new tools. The folders cover both transports (stdio and HTTP) and two ways to build a server: natively with FastMCP, or by converting a FastAPI app.

## Index

| # | Concept | Folder | Script | Transport |
|---|---|---|---|---|
| 01 | stdio MCP server | [`01_stdio_server`](01_stdio_server/) | `calculator_mcp.py` | stdio |
| 02 | HTTP MCP server | [`02_http_server`](02_http_server/) | `fcc_feed_mcp.py` | Streamable HTTP on `:8000/mcp` |
| 03 | FastAPI → MCP | [`03_fastapi_to_mcp`](03_fastapi_to_mcp/) | `fastapi_calculator.py` | Streamable HTTP on `:8000/mcp` |

## Setup

```bash
uv venv
uv pip install -r requirements.txt
```

Dependencies: `fastmcp`, `fastapi`, `fastapi-mcp`, `uvicorn` and `feedparser`.

## Client configuration

Two config files register the servers with MCP clients:

| File | Client |
|---|---|
| [`.mcp.json`](.mcp.json) | Claude Code (project-scoped servers) |
| [`.vscode/mcp.json`](.vscode/mcp.json) | VS Code |

Both register `calculator_mcp` (stdio, started from `.venv`) and `freecodecamp_feed_searcher_mcp` (HTTP, bridged with `npx mcp-remote`). The paths are absolute (`C:/AI Engineering/MCP/...`), so update them if you clone the repo somewhere else.
