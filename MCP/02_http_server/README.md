# 02 · HTTP MCP Server

Running an MCP server as a standalone web service over the Streamable HTTP transport, so one server can be shared by several clients or hosted remotely.

| File | What it does |
|---|---|
| [`fcc_feed_mcp.py`](fcc_feed_mcp.py) | A FastMCP server with two tools that search freeCodeCamp's public RSS feeds: `search_fcc_feed` (news articles, matched on title and description) and `search_fcc_youtube_feed` (YouTube videos, matched on title). It serves on `http://localhost:8000/mcp`. |

## Key ideas

- `mcp.run(transport="http", host=..., port=...)` switches from stdio to HTTP without changing any tool code.
- Clients that only speak stdio can still connect through the `mcp-remote` bridge, as configured in [`../.mcp.json`](../.mcp.json):
  `npx mcp-remote http://localhost:8000/mcp`
- The tools wrap a live external data source, which is the typical reason to build an MCP server.

## Run

```bash
python 02_http_server/fcc_feed_mcp.py
```

Keep it running, then start your MCP client, where it shows up as `freecodecamp_feed_searcher_mcp`. It uses port 8000, like [`03_fastapi_to_mcp`](../03_fastapi_to_mcp/), so run only one of them at a time.
