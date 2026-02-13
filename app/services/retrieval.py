# app/services/retrieval.py
import chromadb
from chromadb.utils import embedding_functions
import os

# CONFIG
PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "fan_manual"
TOP_K = 5

# Initialize Chroma
embedding_func = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

chroma_client = chromadb.PersistentClient(path=PERSIST_DIR)

def get_collection():
    """Get the Chroma collection"""
    return chroma_client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_func
    )

def retrieve(query, top_k=TOP_K):
    """Retrieve documents from Chroma DB"""
    collection = get_collection()
    res = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    docs = []
    for idx in range(len(res["documents"][0])):
        docs.append({
            "text": res["documents"][0][idx],
            "meta": res["metadatas"][0][idx],
            "score": res["distances"][0][idx]
        })
    return docs
