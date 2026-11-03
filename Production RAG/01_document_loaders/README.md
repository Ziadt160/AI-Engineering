# 01 · Document Loaders

The first step of every RAG pipeline: turning raw sources into LangChain `Document` objects, each with `page_content` (the text) and `metadata` (where it came from).

| File | What it does |
|---|---|
| [`document_loaders.py`](document_loaders.py) | `TextLoader` on `files/hello.txt`, `PyPDFLoader` on `files/sample_employee_handbook.pdf`, and `DirectoryLoader` over every PDF in `files/`. Prints the content and metadata of each document. |

## Key ideas

- `PyPDFLoader` returns **one document per page**, with `source` and `page` in the metadata. That's what lets a RAG answer cite a page later.
- `DirectoryLoader(path, glob="*.pdf", loader_cls=PyPDFLoader)` loads a whole folder with a single loader class.

## Run

Uncomment one of the `test_*()` calls at the bottom of the file, then:

```bash
uv run python 01_document_loaders/document_loaders.py
```

The script finds `files/` relative to the current directory, so run it from `Production RAG/`.
