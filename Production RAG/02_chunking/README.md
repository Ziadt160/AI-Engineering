# 02 · Chunking

Splitting long documents into smaller pieces before they are embedded. Chunk size and overlap decide what the retriever can find: chunks that are too small lose context, and chunks that are too large mix unrelated topics.

| File | What it does |
|---|---|
| [`text_splitters.py`](text_splitters.py) | `RecursiveCharacterTextSplitter` (size 100, overlap 50) on a Markdown machine-learning sample; prints chunk count and sizes. Also imports the Character, Token and Markdown-header splitters and a code sample for further experiments. |
| [`test_semantic_chunking.py`](test_semantic_chunking.py) | Compares `SemanticChunker` (percentile breakpoint at 90) with recursive splitting on the same text, plus a table showing which chunk each sentence ends up in. |
| [`prod_ready.py`](prod_ready.py) | "Smart chunking": tries semantic chunking and falls back to recursive splitting if it fails or produces a chunk over the size limit. It then indexes the chunks in Chroma and runs a similarity search. |

## Key ideas

- The recursive splitter tries separators in order (`"\n\n"`, `"\n"`, `". "`, `" "`), so it breaks at paragraphs first and words last.
- Semantic chunking embeds sentences and splits where the meaning changes. The demo text mixes machine-learning sentences with quantum-computing ones, so the comparison table shows whether each strategy separates the two topics.
- In production, keep a deterministic fallback for when the semantic path fails or overshoots the size limit.

## Run

```bash
uv run python 02_chunking/test_semantic_chunking.py
```

`test_semantic_chunking.py` and `prod_ready.py` need the BGE embedding model (see the [track README](../README.md#embedding-model)).
