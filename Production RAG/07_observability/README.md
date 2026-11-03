# 07 · Observability

Tracing every LLM call so you can see the inputs, outputs, latency and token usage of each step in LangSmith.

| File | What it does |
|---|---|
| [`test_langsmith.py`](test_langsmith.py) | Wraps a prompt → LLM → parser chain in `@traceable(name="testing", tags=["quantum"])`, so each call shows up as a named, tagged trace in LangSmith. |

## Key ideas

- With `LANGSMITH_TRACING=true`, LangChain runnables are traced automatically. `@traceable` adds your own functions as parent spans.
- Tags and names make it easy to filter traces by feature or experiment.
- The same decorator is used in [`06_advanced_retrieval/test_compress_contexual_reteriver.py`](../06_advanced_retrieval/test_compress_contexual_reteriver.py) to trace a retriever.

## Run

```bash
uv run python 07_observability/test_langsmith.py
```

Needs `LANGSMITH_API_KEY`, `LANGSMITH_TRACING`, `LANGSMITH_PROJECT` and `LANGSMITH_ENDPOINT` in `.env`.
