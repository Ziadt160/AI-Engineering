import chromadb

client = chromadb.Client()

collection_name = "my_collection"

# create/get a collection
collection = client.get_or_create_collection(name=collection_name)

#documents

docs = [
    {"id": "doc1", "text": "This is the first document."},
    {"id": "doc2", "text": "This is the second document."},
    {"id": "doc3", "text": "This is the third document."}
]

# upsert documents into the collection
for doc in docs:
    collection.upsert(ids=[doc["id"]], documents=[doc["text"]])

query = "first document"


# perform a query on the collection
results = collection.query(query_texts=[query], n_results=2)

print(f"Query results for '{query}':")
print(results)
