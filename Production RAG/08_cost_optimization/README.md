# 08 · Cost Optimization

Three patterns for cutting LLM spend in production: don't call the model twice for the same question, don't use the expensive model for easy questions, and cap how many tokens a request may use.

| File | What it does |
|---|---|
| [`cost_optimization.py`](cost_optimization.py) | `SemanticCache`, `ModelRouting`, and `TokenBudget` with `LLMBudgeted` (described below). |

| Class | Pattern |
|---|---|
| `SemanticCache` | Caches responses by query **meaning**: a new query reuses a stored answer when cosine similarity ≥ `threshold` (default 0.9). Thread-safe, with LRU eviction (`max_size`) and an optional TTL. `get_or_compute()` embeds the query only once. |
| `ModelRouting` | A cheap classifier (`gpt-4o-mini`) labels each query `simple` or `complex` and routes it to `gpt-4o-mini` or `gpt-4o`. Returns the answer, the model used and a rough cost estimate. |
| `TokenBudget` / `LLMBudgeted` | Estimates tokens (words × 1.3), rejects requests over a per-request limit and records usage totals. |

## Usage

The module has no `__main__`. Import the classes instead:

```python
from cost_optimization import SemanticCache

cache = SemanticCache(threshold=0.9, max_size=1000, ttl_seconds=3600)
answer = cache.get_or_compute("What is RAG?", lambda q: llm.invoke(q).content)
```

## Status

`SemanticCache` is complete. The other classes are still work in progress:
- `TokenBudget.record_usage` uses `+-` instead of `+=` for output tokens, so they are never added up.
- `check_token_budget` returns `True` when the text is **over** budget, but `LLMBudgeted.invoke` treats it as "within budget". The error message also refers to `self.budget.max_per_request`, which doesn't exist, and `invoke` doesn't return the response.
- `ModelRouting.invoke` leaves `model` unset if the classifier answers anything other than `simple` or `complex`.
