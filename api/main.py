import logging
from fastapi import FastAPI
from connectors.gdrive import list_files

# Setup basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Google Drive RAG API")

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
        
    logger.info(f"Successfully retrieved {len(result.get('files', []))} files.")
    return result
