# 09 · Production RAG

Packaging the pipeline as a reusable service: configuration in one place, heavy resources created lazily, and a chain built once and reused across requests.

| File | What it does |
|---|---|
| [`subpase_production_rag.py`](subpase_production_rag.py) | Draft `RagProduction` class with a `Config` dataclass, lazily loaded BGE embeddings, a lazily created `PGVector` store on Supabase and a cached LCEL chain. |

## Design

- **`Config`**: connection string, model names, `search_k` and collection name, all in one place.
- **Lazy properties**: the embedding model and database connection are only created the first time they're used, which keeps startup fast and imports cheap.
- **Cached chain**: `_create_chain()` runs once and is then reused through the `chain` property.

## Status: work in progress (does not run yet)

- `@dataclasses` should be `@dataclasses.dataclass`, and the dict defaults need `field(default_factory=...)`.
- It reads `POSTGRES_CONNECTION_URL`, but `.env` defines `POSTGRES_CONNECTION_URI`.
- The `vector_store` property assigns to `self.vector_store` instead of `self._vector_store`.
- `RunnablePassThrough` should be `RunnablePassthrough`, and `Str` should be `StrOutputParser()`.
- `format_docs` is never applied to the retriever output, and `_create_chain()` doesn't return the chain.
- `__init__(self, config: Optional[Config])` needs a default of `None`.
