# 04 · Vector Stores

Where embeddings live and get searched. These scripts cover a local in-memory store (Chroma) and a managed Postgres with pgvector (Supabase).

| File | What it does |
|---|---|
| [`test_chromadb.py`](test_chromadb.py) | Raw `chromadb` client: creates an in-memory collection, upserts three documents and queries by text using Chroma's built-in embedding function. |
| [`supabase.py`](supabase.py) | LangChain `PGVector` on a Supabase Postgres database. It builds the SQLAlchemy URL from environment variables (driver `postgresql+psycopg`, `sslmode=require`) and runs a similarity search on the `tech_docs` collection. |

## Key ideas

- Chroma is the quickest way to experiment: no server, and data stays in memory or in a temp directory.
- pgvector keeps vectors next to your relational data and supports metadata filtering through JSONB (`use_jsonb=True`).
- The password is kept out of the connection string and injected with `make_url(...).set(password=...)`.

## Notes

`supabase.py` splits `TECH_DOCS` into chunks but never calls `vector_store.add_documents(chunks)`. The search only returns results if the `tech_docs` collection was already filled.

## Run

```bash
uv run python 04_vector_stores/test_chromadb.py
uv run python 04_vector_stores/supabase.py
```

`supabase.py` needs `POSTGRES_PASSWORD` and `POSTGRES_CONNECTION_URI` in `.env`.
