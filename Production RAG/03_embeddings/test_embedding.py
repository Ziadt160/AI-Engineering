from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np


embeddings = HuggingFaceEmbeddings(
        model_name=r"C:\Users\pc\.cache\huggingface\hub\models--BAAI--bge-large-en-v1.5\snapshots\d4aa6901d3a41ba39fb536a557fa166f842b0e09",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
        query_encode_kwargs={
            "normalize_embeddings": True,
            "prompt": "Represent this sentence for searching relevant passages: ",
        },
    )

def test_huggingface_embeddings():

    

    query = "What is machine learning?"

    embedding_vector = embeddings.embed_query(query)

    print(f" First 5 values of the embedding vector for the query '{query}': {embedding_vector[:5]}")

    print(f" Length of the embedding vector: {len(embedding_vector)}")

    print(f" Norm of the embedding vector: {np.linalg.norm(embedding_vector)}")


def test_huggingface_embeddings_batch():

    queries = [
        "What is machine learning?",
        "Explain the concept of reinforcement learning.",
        "What are the applications of natural language processing?"
    ]

    embedding_vectors = embeddings.embed_documents(queries)

    for i, query in enumerate(queries):
        print(f" First 5 values of the embedding vector for the query '{query}': {embedding_vectors[i][:5]}")
        print(f" Length of the embedding vector: {len(embedding_vectors[i])}")
        print(f" Norm of the embedding vector: {np.linalg.norm(embedding_vectors[i])}\n")


def test_huggingface_embeddings_similarity():

    docs = [
        "Machine Learning (ML) is a subset of Artificial Intelligence (AI) that focuses on developing algorithms and computational models that enable computers to learn patterns and relationships from data without being explicitly programmed for every possible situation. Instead of relying entirely on predefined rules, machine learning systems use data to identify patterns, make predictions, classify information, or make decisions. The learning process typically involves providing a model with data, allowing it to identify useful patterns or representations within that data, and then using what it has learned to perform a task on new, previously unseen data. The model's performance can be evaluated using appropriate metrics, and its parameters can be adjusted during training to improve its ability to generalize.",
        "Reinforcement learning is a type of machine learning where an agent learns to make decisions by interacting with an environment.",
        "Natural language processing is a field of study that focuses on the interaction between computers and human language."
    ]

    query = "What is machine learning?"

    doc_embeddings = embeddings.embed_documents(docs)
    query_embedding = embeddings.embed_query(query)

    def cosine_similarity(vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    similarities = [cosine_similarity(query_embedding, doc_embedding) for doc_embedding in doc_embeddings]

    scores = sorted(zip(docs, similarities), key=lambda x: x[1], reverse=True)

    print(f"Query: '{query}'\n")
    print("Documents ranked by similarity:")

    for doc, score in scores:
        print(f"Score: {score:.4f} - Document: '{doc}'")


if __name__ == "__main__":
    # test_huggingface_embeddings()
    # test_huggingface_embeddings_batch()
    test_huggingface_embeddings_similarity()