from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import chromadb
from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction
from chromadb.config import Settings
import time
import config

def ingest_pdf(pdf_path: str = "../data/rules.pdf"):
    print(f"Loading {pdf_path}...")
    
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    print(f"Loaded {len(pages)} pages")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len
    )
    chunks = splitter.split_documents(pages)
    print(f"Split into {len(chunks)} chunks")
    
    # LangChain embeddings (handles the new google.genai under the hood)
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=config.GOOGLE_API_KEY
    )
    
    # ChromaDB client (new API)
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection("university_rules")
    
    BATCH_SIZE = 3
    DELAY = 4.0
    
    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    
    total = len(chunks)
    for i in range(0, total, BATCH_SIZE):
        batch_end = min(i + BATCH_SIZE, total)
        print(f"Processing batch {i//BATCH_SIZE + 1}/{(total-1)//BATCH_SIZE + 1} (chunks {i}-{batch_end-1})...")
        
        # Generate embeddings for this batch
        batch_texts = texts[i:batch_end]
        batch_embeddings = embeddings.embed_documents(batch_texts)
        
        # Add to Chroma
        collection.add(
            documents=batch_texts,
            embeddings=batch_embeddings,
            metadatas=metadatas[i:batch_end],
            ids=ids[i:batch_end]
        )
        
        if batch_end < total:
            time.sleep(DELAY)
    
    print(f"✅ Ingested {total} chunks into ChromaDB")
    return collection

if __name__ == "__main__":
    ingest_pdf()