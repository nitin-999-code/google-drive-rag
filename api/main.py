import logging
from fastapi import FastAPI
from pydantic import BaseModel
from connectors.gdrive import list_files
from api.rag_service import process_documents, answer_query

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Google Drive RAG API")

class AskRequest(BaseModel):
    query: str

@app.get("/")
def health_check():
    return {"message": "Google Drive RAG API running"}

@app.post("/sync-drive")
def sync_drive():
    logger.info("Sync drive endpoint called.")
    result = list_files()
    
    if result.get("status") == "error":
        logger.error(f"Failed to sync drive: {result.get('message')}")
        return result
        
    files = result.get('files', [])
    count = process_documents(files)
    
    return {
        "status": "success",
        "processed_files": count,
        "total_files": len(files)
    }

@app.post("/ask")
def ask(request: AskRequest):
    logger.info(f"Ask endpoint called with query: {request.query}")
    return answer_query(request.query)
