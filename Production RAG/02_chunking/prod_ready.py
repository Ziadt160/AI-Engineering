from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores.chroma import Chroma
import tempfile
from dotenv import load_dotenv


embeddings = HuggingFaceEmbeddings(
        model_name=r"C:\Users\pc\.cache\huggingface\hub\models--BAAI--bge-large-en-v1.5\snapshots\d4aa6901d3a41ba39fb536a557fa166f842b0e09",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )


text = """
A: Machine learning uses statistical methods to learn patterns.

B: Neural networks are one of the most popular machine learning models.

C: Transformers use attention mechanisms to process sequences.

D: Quantum computers use qubits instead of classical bits.

E: Qubits can exist in superposition.
"""

def _recursive_fallback():
    recursive_chunker = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20, separators=["\n\n", "\n", ". ", " "])
    return recursive_chunker.split_text(text)


def smart_chunking(
        is_semantic: bool = False,
        max_chunk_size: int = 100
):

    if is_semantic:

        try:

            semantic_chunker = SemanticChunker(
                embeddings=embeddings,
                breakpoint_threshold_type="percentile",
                breakpoint_threshold_amount=90
            )

            chunks = semantic_chunker.split_text(text)

            if (any(len(c) > max_chunk_size for c in chunks)):
                return _recursive_fallback()

            return chunks
        except Exception as e:
            print(f" Semantic chunking failed : {e}, using fallback")
            return _recursive_fallback()


    return _recursive_fallback()


chunks = smart_chunking(True, 100)

vector_store = Chroma.from_texts(chunks, embedding=embeddings, collection_name="smart_chunk")

q = "Explain to me Machine learnign"

chunk = vector_store.similarity_search(q, 1)

print(chunk[0])