# 03 · Embeddings

Turning text into vectors whose distance reflects meaning. Every chunk is embedded once at indexing time, and every query is embedded at search time.

| File | What it does |
|---|---|
| [`test_embedding.py`](test_embedding.py) | `BAAI/bge-large-en-v1.5` through `HuggingFaceEmbeddings`. It embeds one query (1024 dimensions, norm 1.0), embeds a batch, and ranks documents against a query by cosine similarity. |
| [`cached_embedding.py`](cached_embedding.py) | Wraps the model in `CacheBackedEmbeddings` with a `LocalFileStore`, so text that was already embedded is read from disk instead of recomputed. |

## Key ideas

- With `normalize_embeddings=True`, the dot product equals cosine similarity.
- BGE models expect an instruction prefix on **queries only** ("Represent this sentence for searching relevant passages: "), set through `query_encode_kwargs`.
- Caching embeddings is one of the cheapest cost and latency wins when re-indexing.

## Notes

- `cached_embedding.py` reads the model name from `EMBEDDING_MODEL_NAME` in `.env`.
- By default, `CacheBackedEmbeddings` caches `embed_documents` only. The script passes `query_embedding_cache=True` so the second `embed_query` call comes from the cache.

## Run

```bash
uv run python 03_embeddings/test_embedding.py
```
