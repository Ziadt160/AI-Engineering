from langchain_core.documents import Document
from langchain_community.vectorstores.chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


from langchain_core.documents import Document

embedding = HuggingFaceEmbeddings(
    model_name=r"C:\Users\pc\.cache\huggingface\hub\models--BAAI--bge-large-en-v1.5\snapshots\d4aa6901d3a41ba39fb536a557fa166f842b0e09",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

documents = [
    Document(
        page_content="""
        Machine learning is a branch of artificial intelligence that enables
        computers to learn patterns from data without being explicitly programmed.
        Supervised learning uses labeled datasets to train predictive models.
        """,
        metadata={"topic": "machine-learning", "id": "doc1"}
    ),

    Document(
        page_content="""
        Neural networks are computational models inspired by biological neurons.
        A neural network consists of layers of interconnected nodes. Deep learning
        uses neural networks with multiple hidden layers to learn complex patterns.
        """,
        metadata={"topic": "deep-learning", "id": "doc2"}
    ),

    Document(
        page_content="""
        Retrieval-Augmented Generation, commonly called RAG, combines information
        retrieval with large language models. A RAG system retrieves relevant
        documents from a knowledge base and provides them as context to an LLM.
        """,
        metadata={"topic": "rag", "id": "doc3"}
    ),

    Document(
        page_content="""
        Hybrid search combines lexical retrieval methods such as BM25 with
        semantic vector search. BM25 is particularly effective when the query
        contains exact terms, names, identifiers, or technical terminology.
        """,
        metadata={"topic": "information-retrieval", "id": "doc4"}
    ),

    Document(
        page_content="""
        Vector databases store numerical representations called embeddings.
        These embeddings allow systems to find documents that are semantically
        similar even when they do not share the same words with the query.
        """,
        metadata={"topic": "vector-database", "id": "doc5"}
    ),

    Document(
        page_content="""
        BM25 is a probabilistic ranking algorithm commonly used for information
        retrieval. It scores documents according to term frequency, inverse
        document frequency, and document length normalization.
        """,
        metadata={"topic": "bm25", "id": "doc6"}
    ),

    Document(
        page_content="""
        Dense retrieval represents queries and documents as dense vectors.
        A similarity function such as cosine similarity can then be used to
        retrieve documents with related meanings.
        """,
        metadata={"topic": "dense-retrieval", "id": "doc7"}
    ),

    Document(
        page_content="""
        Reciprocal Rank Fusion, or RRF, is a method for combining rankings from
        multiple retrieval systems. It can be used to combine BM25 rankings
        with vector similarity rankings in a hybrid retrieval pipeline.
        """,
        metadata={"topic": "ranking", "id": "doc8"}
    ),

    Document(
        page_content="""
        LangChain provides abstractions for document loaders, text splitters,
        retrievers, vector stores, and retrieval-augmented generation pipelines.
        These components can be combined to build sophisticated search systems.
        """,
        metadata={"topic": "langchain", "id": "doc9"}
    ),

    Document(
        page_content="""
        Chunking divides large documents into smaller pieces before indexing.
        Chunk size and overlap affect retrieval quality because chunks that are
        too small may lose context while very large chunks may contain unrelated
        information.
        """,
        metadata={"topic": "chunking", "id": "doc10"}
    ),
]

vector_store = Chroma.from_documents(documents, embedding=embedding, collection_name="hybrid_search_docs")
vector_store_retriever = vector_store.as_retriever(search_kwargs={"k" : 3})
bm25_retriever = BM25Retriever.from_documents(documents=documents, k=3)

ensemeble_retriever = EnsembleRetriever(
    retrievers=[vector_store_retriever, bm25_retriever],
    weights=[0.5, 0.5]
)


query = "What is BM25"

results = ensemeble_retriever.invoke(query)

print(results)
