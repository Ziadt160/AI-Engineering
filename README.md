# AI Engineering

Hands-on code and notes from learning AI engineering, organized by concept. There are two tracks:

- **[Production RAG](Production%20RAG/)**: retrieval-augmented generation with LangChain, from document loading to caching, routing and tracing.
- **[MCP](MCP/)**: Model Context Protocol servers that give LLM clients new tools.

Each concept has its own folder with an index README that explains the idea, lists the scripts and shows how to run them.

## Index

### Production RAG

| # | Concept | What you'll find |
|---|---|---|
| 00 | [Setup](Production%20RAG/00_setup/) | Environment and LLM provider check |
| 01 | [Document loaders](Production%20RAG/01_document_loaders/) | Text, PDF and directory loaders |
| 02 | [Chunking](Production%20RAG/02_chunking/) | Recursive and semantic chunking, with a fallback strategy |
| 03 | [Embeddings](Production%20RAG/03_embeddings/) | BGE embeddings, cosine similarity, embedding cache |
| 04 | [Vector stores](Production%20RAG/04_vector_stores/) | Chroma, and PGVector on Supabase |
| 05 | [Basic RAG](Production%20RAG/05_basic_rag/) | End-to-end LCEL RAG chain, answers with sources |
| 06 | [Advanced retrieval](Production%20RAG/06_advanced_retrieval/) | Hybrid (BM25 + vector), multi-query, parent-document, contextual compression |
| 07 | [Observability](Production%20RAG/07_observability/) | LangSmith tracing |
| 08 | [Cost optimization](Production%20RAG/08_cost_optimization/) | Semantic cache, model routing, token budgets |
| 09 | [Production RAG](Production%20RAG/09_production_rag/) | Service-style RAG class on Supabase |

### MCP

| # | Concept | What you'll find |
|---|---|---|
| 01 | [stdio MCP server](MCP/01_stdio_server/) | FastMCP calculator over stdio |
| 02 | [HTTP MCP server](MCP/02_http_server/) | FastMCP freeCodeCamp feed search over Streamable HTTP |
| 03 | [FastAPI → MCP](MCP/03_fastapi_to_mcp/) | Turning a FastAPI app into MCP tools with `fastapi-mcp` |

## Repository layout

```
AI Engineering/
├── MCP/
│   ├── 01_stdio_server/
│   ├── 02_http_server/
│   ├── 03_fastapi_to_mcp/
│   ├── .mcp.json, .vscode/mcp.json   # client configs
│   └── requirements.txt
└── Production RAG/
    ├── 00_setup/ … 09_production_rag/
    ├── files/                        # generic sample documents
    ├── .env.example
    └── pyproject.toml, uv.lock
```

## Secrets

API keys go in `Production RAG/.env`, which is git-ignored. [`Production RAG/.env.example`](Production%20RAG/.env.example) lists the variables you need.
