# 06 · Advanced Retrieval

Techniques that improve on plain top-k vector search when queries use exact terms, are phrased differently from the documents, or the right answer is buried in a long chunk.

| File | Technique | What it does |
|---|---|---|
| [`hybrid_search.py`](hybrid_search.py) | Hybrid search | Combines BM25 (keyword) and Chroma (vector) retrievers with `EnsembleRetriever`, weighted 0.5 / 0.5 and merged by reciprocal rank fusion. |
| [`multi_query_test.py`](multi_query_test.py) | Multi-query | `MultiQueryRetriever` has an LLM rewrite the question into several variants, retrieves for each one and merges the unique results. |
| [`test_parent_child_reteriver.py`](test_parent_child_reteriver.py) | Parent-document | `ParentDocumentRetriever` searches small child chunks (200 chars) but returns their larger parent chunks (800 chars) from an `InMemoryStore`. |
| [`test_compress_contexual_reteriver.py`](test_compress_contexual_reteriver.py) | Contextual compression | `ContextualCompressionRetriever` with `LLMChainExtractor`: retrieves chunks, then has an LLM keep only the sentences relevant to the query. Traced with LangSmith `@traceable`. |

## When to use which

- **Hybrid**: queries with names, IDs, error codes or jargon that embeddings blur together.
- **Multi-query**: short or ambiguous questions, when recall matters more than latency.
- **Parent-document**: precise matching on small chunks while still giving the LLM enough surrounding context.
- **Compression**: long, noisy chunks where only a sentence or two is relevant (it costs one LLM call per retrieved chunk).

## Run

```bash
uv run python 06_advanced_retrieval/hybrid_search.py
```

The multi-query and compression scripts need `OPENROUTER_API_KEY`.
