from langchain.tools import tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import chromadb
import os

from .config import GOOGLE_API_KEY

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

@tool
def search_rules(query: str) -> str:
    """
    Search the university rulebook for policies and regulations.
    ...
    """
    try:

        client = chromadb.PersistentClient(path=CHROMA_PATH)

        collection = client.get_collection("university_rules")

        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=GOOGLE_API_KEY
        )

        query_embedding = embeddings.embed_query(query)

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5
        )

        if not results["documents"][0]:
            return "No relevant rules found."

        formatted = []

        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            page = meta.get("page", "unknown")
            formatted.append(f"[Page {page}] {doc}")

        return "\n\n".join(formatted)

    except Exception as e:
        return f"Error searching rules: {str(e)}"