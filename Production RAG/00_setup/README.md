# 00 · Setup

Checks that the Python environment and the LLM provider are wired up before anything else is built.

| File | What it does |
|---|---|
| [`main.py`](main.py) | Prints the installed `langchain-core` and `langgraph` versions, then sends one prompt to `gpt-4o-mini` through OpenRouter and expects "setup complete" back. |

## Run

```bash
uv run python 00_setup/main.py
```

Needs `OPENROUTER_API_KEY` in `.env`.
