# 05 · Basic RAG

Putting the pieces together: load, split, embed, index, retrieve, and generate an answer grounded in the retrieved context, wired up with LangChain Expression Language (LCEL).

| File | What it does |
|---|---|
| [`basic_rag.py`](basic_rag.py) | End-to-end pipeline. It loads every PDF in `files/`, splits them (size 500, overlap 200), embeds with BGE, indexes in Chroma, retrieves the top 2 chunks and answers with `gpt-4o-mini`. The default question is "How many days of paid annual leave do employees get?" (the sample handbook says 20). |
| [`demo_rag_with_sources.py`](demo_rag_with_sources.py) | A RAG chain that prefixes each retrieved chunk with its `source` metadata and asks the model to cite sources. It also shows Chroma HNSW tuning through `collection_metadata`. |

## Key ideas

- The chain shape is `{"context": retriever | format_docs, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()`.
- The prompt tells the model to say "I don't know" when the answer is not in the context, which is the simplest guard against hallucination.
- Citations are only as good as the metadata: the loader's `source` and `page` fields have to make it into the prompt.

## Notes

In `demo_rag_with_sources.py`:
- The sample documents have no `source` key, so citations show as `[unknown]`.
- The `hnsfw:construction_ef` key is misspelled (it should be `hnsw:construction_ef`), so Chroma ignores that setting.

## Run

```bash
uv run python 05_basic_rag/basic_rag.py
```

Run it from `Production RAG/` so that `./files` resolves.
