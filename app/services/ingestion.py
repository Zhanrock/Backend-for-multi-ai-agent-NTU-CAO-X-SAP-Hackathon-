# app/services/ingestion.py
import os
import re
import pdfplumber
import chromadb
from chromadb.utils import embedding_functions

# ----------- CONFIG -----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PDF_PATH = os.path.join(BASE_DIR, "docs", "FAN_Manual.pdf")
CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "fan_manual"

# ------------------------------

def load_manual(path):
    """Read all PDF with pdfplumber"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def split_sections(text):
    """
    split according to heading both head (1., 2.) and section (1.1, 5.4, ...)
    use regex to prevent .1, .2 to output single section
    """
    parts = re.split(r"\n(?=\d+(?:\.\d+)*\s+)", text)
    sections = [p.strip() for p in parts if p.strip()]
    return sections

def ingest_to_chroma(sections):
    """
    Create/Connect Chroma DB then add persist sections
    """
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)

    # Use OpenAI embedding
    embedding_func = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )

    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION_NAME)
    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_func
    )

    # add batch
    for i, sec in enumerate(sections):
        first_line = sec.split("\n", 1)[0]
        title = re.sub(r"^\d+(?:\.\d+)*\s+", "", first_line).strip()

        collection.add(
            documents=[sec],
            metadatas=[{"title": title}],
            ids=[f"sec-{i}"]
        )

        # debug print
        print(f"Ingested section {i}: {title}")

    return len(sections)

if __name__ == "__main__":
    text = load_manual(PDF_PATH)
    sections = split_sections(text)
    n = ingest_to_chroma(sections)
    print(f"Persisted {n} sections into Chroma at {CHROMA_DB_DIR}")
