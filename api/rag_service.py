import os
import io
import json
import logging
from googleapiclient.http import MediaIoBaseDownload
from connectors.gdrive import get_drive_service
from processing.parser import extract_text
from processing.chunker import chunk_text
from embedding.embedder import generate_embeddings, model
from search.vector_store import store_embeddings, search_similar

logger = logging.getLogger(__name__)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

PROCESSED_FILE_PATH = os.path.join(DATA_DIR, "processed_files.json")

def load_processed_files():
    if not os.path.exists(PROCESSED_FILE_PATH):
        return set()
    with open(PROCESSED_FILE_PATH, "r") as f:
        data = json.load(f)
    return set(data.get("processed_files", []))

def save_processed_files(files):
    with open(PROCESSED_FILE_PATH, "w") as f:
        json.dump(
            {"processed_files": list(files)},
            f,
            indent=2
        )

SUPPORTED_MIME_TYPES = [
    "application/pdf",
    "text/plain"
]
PROCESSED_FILES = load_processed_files()

def download_file(file):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    service = get_drive_service()
    file_id = file["id"]
    file_name = file["name"]
    file_path = os.path.join(DATA_DIR, file_name)
    
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    
    with open(file_path, "wb") as f:
        f.write(fh.getvalue())
        
    return file_path

def process_documents(files, force_reindex=False):
    if force_reindex:
        logger.info("Force reindex enabled — clearing existing index")
        
        if os.path.exists("data/index.faiss"):
            os.remove("data/index.faiss")
            
        if os.path.exists("data/documents.pkl"):
            os.remove("data/documents.pkl")
            
        PROCESSED_FILES.clear()
        
        import search.vector_store as vector_store
        vector_store.index = None
        vector_store.chunk_mapping.clear()
        vector_store.chunk_sources.clear()

    processed_count = 0
    for file in files:
        file_name = file["name"]
        mime_type = file["mimeType"]
        
        msg = f"Found file: {file_name} {mime_type}"
        print(msg)
        logger.info(msg)
        
        if mime_type not in SUPPORTED_MIME_TYPES:
            msg = f"Skipping unsupported file: {file_name}"
            print(msg)
            logger.info(msg)
            continue
            
        if not force_reindex and file_name in PROCESSED_FILES:
            msg = f"Already indexed: {file_name}"
            print(msg)
            logger.info(msg)
            continue
            
        try:
            file_path = download_file(file)
            msg = f"Downloaded: {file_name}"
            print(msg)
            logger.info(msg)
            
            text = extract_text(file_path)
            if not text:
                msg = f"No text extracted: {file_name}"
                print(msg)
                logger.info(msg)
                continue
                
            chunks = chunk_text(text)
            if not chunks:
                msg = f"No chunks generated: {file_name}"
                print(msg)
                logger.info(msg)
                continue
                
            embeddings = generate_embeddings(chunks)
            store_embeddings(embeddings, chunks, file_name)
            
            PROCESSED_FILES.add(file_name)
            save_processed_files(PROCESSED_FILES)
            processed_count += 1
            
            msg = f"Processed: {file_name}"
            print(msg)
            logger.info(msg)
        except Exception as e:
            msg = f"Error processing {file_name} {str(e)}"
            print(msg)
            logger.error(msg)
            
    return processed_count

def answer_query(query):
    query_embedding = model.encode([query])[0]
    chunks, sources = search_similar(query, query_embedding, top_k=5)
    
    if not chunks:
        return {
            "answer": "No relevant documents found.",
            "sources": []
        }
        
    context = "\n...\n".join(chunks)
    answer = f"Based on the following context:\n\n{context}"
    
    unique_sources = list(set(sources))
    return {
        "answer": answer,
        "sources": unique_sources
    }
