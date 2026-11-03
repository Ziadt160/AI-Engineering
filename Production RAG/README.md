# Production RAG

A step-by-step track for building retrieval-augmented generation (RAG) with LangChain, from loading a single PDF to a production-style service with caching, routing and tracing. Each numbered folder covers one concept and has its own README.

## Index

| # | Concept | Folder | Scripts |
|---|---|---|---|
| 00 | Setup | [`00_setup`](00_setup/) | `main.py` |
| 01 | Document loaders | [`01_document_loaders`](01_document_loaders/) | `document_loaders.py` |
| 02 | Chunking | [`02_chunking`](02_chunking/) | `text_splitters.py`, `test_semantic_chunking.py`, `prod_ready.py` |
| 03 | Embeddings | [`03_embeddings`](03_embeddings/) | `test_embedding.py`, `cached_embedding.py` |
| 04 | Vector stores | [`04_vector_stores`](04_vector_stores/) | `test_chromadb.py`, `supabase.py` |
| 05 | Basic RAG | [`05_basic_rag`](05_basic_rag/) | `basic_rag.py`, `demo_rag_with_sources.py` |
| 06 | Advanced retrieval | [`06_advanced_retrieval`](06_advanced_retrieval/) | `hybrid_search.py`, `multi_query_test.py`, `test_parent_child_reteriver.py`, `test_compress_contexual_reteriver.py` |
| 07 | Observability | [`07_observability`](07_observability/) | `test_langsmith.py` |
| 08 | Cost optimization | [`08_cost_optimization`](08_cost_optimization/) | `cost_optimization.py` |
| 09 | Production RAG | [`09_production_rag`](09_production_rag/) | `subpase_production_rag.py` (work in progress) |

## Setup

Requires Python 3.13 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
cp .env.example .env   # then fill in your keys
```

Run every script **from this folder**, because some of them read `./files`:

```bash
uv run python 05_basic_rag/basic_rag.py
```

## Sample data

[`files/`](files/) holds generic test documents:

| File | Contents |
|---|---|
| `hello.txt` | Two-line text file for the text loader. |
| `sample_employee_handbook.pdf` | 3-page handbook for a fictional company (leave, remote work, expenses, IT security). Good for Q&A such as "How many days of annual leave do employees get?" |
| `sample_rag_guide.pdf` | 2-page overview of RAG concepts (chunking, embeddings, vector stores, advanced retrieval). |

Drop your own PDFs into `files/` to test the pipeline on your documents.

## Embedding model

Most scripts use [`BAAI/bge-large-en-v1.5`](https://huggingface.co/BAAI/bge-large-en-v1.5) and load it from a local Hugging Face snapshot path (`C:\Users\pc\.cache\huggingface\hub\...`). On another machine, replace that path with `"BAAI/bge-large-en-v1.5"`, and the model (about 1.3 GB) downloads on first use.

## Stack

LangChain 1.x · LangGraph · Chroma · PGVector on Supabase · Hugging Face BGE embeddings · OpenRouter (`gpt-4o-mini`, `gpt-4o`) · LangSmith
