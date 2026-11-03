# 03 · FastAPI → MCP

Exposing an existing REST API as MCP tools without rewriting it. `fastapi-mcp` reads the FastAPI routes and publishes each endpoint as a tool.

| File | What it does |
|---|---|
| [`fastapi_calculator.py`](fastapi_calculator.py) | A regular FastAPI app with `POST /add`, `/subtract`, `/multiply` and `/divide`. `FastApiMCP(app).mount_http()` mounts an MCP endpoint at `/mcp` next to the REST API. |

## Key ideas

- The same app serves both humans and programs (`/docs` for Swagger, plain REST) and AI agents (`/mcp`).
- Endpoint docstrings and parameter types become the tool descriptions and schemas, so good API docs give you good tool docs.
- Compare with [`01_stdio_server`](../01_stdio_server/), which implements the same calculator natively in FastMCP.

## Run

```bash
python 03_fastapi_to_mcp/fastapi_calculator.py
```

- REST docs: http://localhost:8000/docs
- MCP endpoint: http://localhost:8000/mcp (connect with `npx mcp-remote http://localhost:8000/mcp`)

It uses port 8000, like [`02_http_server`](../02_http_server/), so run only one of them at a time.
