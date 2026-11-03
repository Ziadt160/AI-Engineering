from langchain_classic.embeddings.cache import CacheBackedEmbeddings
from langchain_classic.storage import LocalFileStore
from langchain_huggingface import HuggingFaceEmbeddings
from tempfile import mkdtemp
import os
from dotenv import load_dotenv
load_dotenv()

embedding = HuggingFaceEmbeddings(
    model_name = os.getenv("EMBEDDING_MODEL_NAME"),
    model_kwargs={"device" : "cpu"},
    encode_kwargs={"normalize_embeddings" : True}
)

store = LocalFileStore(root_path=mkdtemp())

cached_embedding = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings=embedding,
    document_embedding_cache=store,
    namespace="exercise"
)


query = "What is langchain"

embedding = cached_embedding.embed_query(query)

print("First embedding")

embedding = cached_embedding.embed_query(query)

print("From cache")