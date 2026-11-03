import textwrap

from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()


embeddings = HuggingFaceEmbeddings(
        model_name=r"C:\Users\pc\.cache\huggingface\hub\models--BAAI--bge-large-en-v1.5\snapshots\d4aa6901d3a41ba39fb536a557fa166f842b0e09",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )


text = """A: Machine learning uses statistical methods to learn patterns.

B: Neural networks are one of the most popular machine learning models.

C: Transformers use attention mechanisms to process sequences.

D: Quantum computers use qubits instead of classical bits.

E: Qubits can exist in superposition."""

semantic_chunking = SemanticChunker(embeddings=embeddings, breakpoint_threshold_type="percentile", breakpoint_threshold_amount=90)
# Default chunk_size is 4000, which would keep this short text in a single chunk.
recursive_chunking = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", ". ", " "], chunk_size=150, chunk_overlap=0)

semantic_chunks = semantic_chunking.split_text(text)
recursive_chunks = recursive_chunking.split_text(text)


WIDTH = 80


def print_chunks(title: str, chunks: list[str]) -> None:
    print(f" {title} ({len(chunks)} chunks) ".center(WIDTH, "="))
    for i, chunk in enumerate(chunks, 1):
        print(f"\n[Chunk {i}] {len(chunk)} chars")
        print("-" * WIDTH)
        for line in chunk.splitlines():
            if line.strip():
                print(textwrap.fill(line, WIDTH, initial_indent="  ", subsequent_indent="  "))
    print()


def chunk_of(sentence: str, chunks: list[str]) -> str:
    return next((str(i) for i, c in enumerate(chunks, 1) if sentence in c), "split")


def print_comparison(results: dict[str, list[str]]) -> None:
    names = list(results)
    print(" Comparison ".center(WIDTH, "="))

    print(f"\n{'':<16}" + "".join(f"{n:>14}" for n in names))
    stats = {
        "Chunks": lambda c: len(c),
        "Avg chars": lambda c: round(sum(map(len, c)) / len(c)),
        "Min chars": lambda c: min(map(len, c)),
        "Max chars": lambda c: max(map(len, c)),
    }
    for label, fn in stats.items():
        print(f"{label:<16}" + "".join(f"{fn(results[n]):>14}" for n in names))

    # Which chunk each original sentence landed in: shows where each strategy draws its boundaries.
    print(f"\n{'Sentence':<50}" + "".join(f"{n:>14}" for n in names))
    print("-" * (50 + 14 * len(names)))
    for sentence in (s.strip() for s in text.split("\n\n") if s.strip()):
        short = sentence if len(sentence) <= 47 else sentence[:44] + "..."
        print(f"{short:<50}" + "".join(f"{chunk_of(sentence, results[n]):>14}" for n in names))
    print()


results = {"Semantic": semantic_chunks, "Recursive": recursive_chunks}
for name, chunks in results.items():
    print_chunks(f"{name} chunking", chunks)
print_comparison(results)
