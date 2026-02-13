# app/services/embeddings.py
import os
from chromadb.utils import embedding_functions

def get_openai_embedding_function():
    """Get OpenAI embedding function"""
    return embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )
