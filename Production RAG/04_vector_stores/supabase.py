from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from dotenv import load_dotenv
from sqlalchemy.engine import make_url
import os
load_dotenv()

password = os.getenv("POSTGRES_PASSWORD")
connection_uri = os.getenv("POSTGRES_CONNECTION_URI")
if not password:
    raise RuntimeError("POSTGRES_PASSWORD is not set")
if not connection_uri:
    raise RuntimeError("POSTGRES_CONNECTION_URI is not set")

postgres_connection_url = make_url(connection_uri).set(
    password=password,
    drivername="postgresql+psycopg",
)
postgres_connection_url = postgres_connection_url.set(
    query={**postgres_connection_url.query, "sslmode": "require"}
).render_as_string(hide_password=False)


TECH_DOCS = [
    Document(
        page_content="Python is a high-level programming language known for its simplicity and readability. It supports multiple programming paradigms including procedural, object-oriented, and functional programming. Python is widely used in web development, data science, artificial intelligence, and automation.",
        metadata={
            "topic": "programming",
            "language": "python",
            "difficulty": "beginner",
        },
    ),
    Document(
        page_content="JavaScript is the language of the web. It runs in browsers and on servers with Node.js. Modern frameworks like React, Vue, and Angular make building interactive web applications efficient. JavaScript supports asynchronous programming with Promises and async/await.",
        metadata={
            "topic": "programming",
            "language": "javascript",
            "difficulty": "intermediate",
        },
    ),
    Document(
        page_content="Machine learning is a subset of AI that enables systems to learn from data. Supervised learning uses labeled data, while unsupervised learning finds patterns in unlabeled data. Popular ML frameworks include TensorFlow, PyTorch, and scikit-learn.",
        metadata={
            "topic": "ai",
            "subtopic": "machine_learning",
            "difficulty": "advanced",
        },
    ),
    Document(
        page_content="LangChain is a framework for building LLM applications. It provides tools for prompts, chains, agents, and memory. LangChain supports multiple LLM providers including OpenAI, Anthropic, and local models.",
        metadata={
            "topic": "ai",
            "subtopic": "llm_frameworks",
            "difficulty": "intermediate",
        },
    ),
    Document(
        page_content="LangGraph is a library for building stateful, multi-actor applications with LLMs. Key features include state management, cycles and loops, human-in-the-loop workflows, and persistence. LangGraph extends LangChain for complex agent architectures.",
        metadata={
            "topic": "ai",
            "subtopic": "llm_frameworks",
            "difficulty": "advanced",
        },
    ),
    Document(
        page_content="Docker is a platform for containerizing applications. Containers package code and dependencies together for consistent deployment. Docker Compose orchestrates multi-container applications. Kubernetes scales Docker containers in production.",
        metadata={
            "topic": "devops",
            "subtopic": "containers",
            "difficulty": "intermediate",
        },
    ),
    Document(
        page_content="PostgreSQL is an advanced open-source relational database. It supports JSON data types, full-text search, and extensions like pgvector for vector similarity search. PostgreSQL is ACID compliant and highly extensible.",
        metadata={
            "topic": "database",
            "type": "relational",
            "difficulty": "intermediate",
        },
    ),
    Document(
        page_content="Vector databases like Pinecone, Chroma, and Qdrant are optimized for storing and searching embeddings. They enable semantic similarity search for RAG applications. Most support metadata filtering and hybrid search combining keywords with vectors.",
        metadata={"topic": "database", "type": "vector", "difficulty": "intermediate"},
    ),
]

embedding = HuggingFaceEmbeddings(
        model_name=r"C:\Users\pc\.cache\huggingface\hub\models--BAAI--bge-large-en-v1.5\snapshots\d4aa6901d3a41ba39fb536a557fa166f842b0e09",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
)


recursive_text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=20, separators=["\n\n", "\n", ". ", " "])

chunks = recursive_text_splitter.split_documents(TECH_DOCS)

vector_store = PGVector(
    embeddings=embedding,
    collection_name="tech_docs",
    use_jsonb=True,
    connection=postgres_connection_url

)


docs = vector_store.similarity_search(query="What is langhchain" , k=1)


print(docs)