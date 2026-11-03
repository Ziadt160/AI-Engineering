# 09 · Production RAG

Packaging the pipeline as a reusable service: configuration in one place, heavy resources created lazily, and a chain built once and reused across requests.

| File | What it does |
|---|---|
| [`subpase_production_rag.py`](subpase_production_rag.py) | `RagProduction` class with a `Config` dataclass, lazily loaded BGE embeddings, a lazily created `PGVector` store on Supabase and a cached LCEL chain. |

## Design

- **`Config`**: connection string, model names, `search_k` and collection name, all in one place. The connection string is built from `POSTGRES_CONNECTION_URI` and `POSTGRES_PASSWORD` (driver `postgresql+psycopg`, `sslmode=require`).
- **Lazy properties**: the embedding model and database connection are only created the first time they're used, which keeps startup fast and imports cheap.
- **Cached chain**: `_create_chain()` runs once and is then reused through the `chain` property.

## Usage

The module has no `__main__`. Import the class instead (run from `Production RAG/`):

```python
import sys; sys.path.insert(0, "09_production_rag")
from subpase_production_rag import RagProduction

rag = RagProduction()
print(rag.chain.invoke("What is LangChain?"))
```

It answers from the `production_rag` collection, so fill that collection first (for example with `rag.vector_store.add_documents(...)`).
