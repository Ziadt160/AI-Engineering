# 01 · stdio MCP Server

The simplest MCP transport: the client (Claude Code, Claude Desktop, VS Code) starts the server as a child process and exchanges JSON-RPC messages over stdin/stdout. No ports and no network.

| File | What it does |
|---|---|
| [`calculator_mcp.py`](calculator_mcp.py) | A FastMCP server with four tools: `add_numbers`, `subtract_numbers`, `multiply_numbers` and `divide_numbers` (it raises an error on division by zero). |

## Key ideas

- `@mcp.tool(name=..., description=...)` turns a typed Python function into a tool. FastMCP builds the JSON schema from the type hints, and the model reads the description and docstring to decide when to call it.
- `mcp.run()` defaults to the stdio transport.
- Errors raised inside a tool are sent back to the client as tool errors instead of crashing the server.

## Run

The client normally starts the server. It is registered in [`../.mcp.json`](../.mcp.json) and [`../.vscode/mcp.json`](../.vscode/mcp.json) as `calculator_mcp`. To try it on its own with the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector python 01_stdio_server/calculator_mcp.py
```
