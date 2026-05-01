import os
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'service_account.json'

def get_drive_service():
    """
    Load credentials from service_account.json
    Create Google Drive API service
    Return the service object
    """
    try:
        if not os.path.exists(SERVICE_ACCOUNT_FILE):
            logger.error(f"Credentials file {SERVICE_ACCOUNT_FILE} not found.")
            return None
        
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)
        return service
    except Exception as e:
        logger.error(f"Error creating Drive service: {e}")
        return None

def list_files():
    """
    Fetch the first 10 files from Google Drive
    Return a list of dictionaries containing: id, name, mimeType
    """
    try:
        service = get_drive_service()
        if not service:
            return {
                "status": "error",
                "message": "Failed to create Google Drive service. Check service_account.json."
            }

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])

        files = []
        for item in items:
            files.append({
                "id": item.get("id"),
                "name": item.get("name"),
                "mimeType": item.get("mimeType")
            })
            
        return {
            "status": "success",
            "files": files
        }
    except HttpError as error:
        logger.error(f"An API error occurred: {error}")
        return {
            "status": "error",
            "message": f"Google Drive API error: {error}"
        }
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
