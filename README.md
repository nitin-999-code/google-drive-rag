# Google Drive RAG - Checkpoint 1

## Description:

This service connects to Google Drive using a service account and exposes an API to sync files.

## Setup instructions:

1) Install dependencies:
```bash
pip install -r requirements.txt
```

2) Add `service_account.json` to the root of the project.

3) Run server:
```bash
uvicorn api.main:app --reload
```

## API documentation:

`POST /sync-drive`
Syncs files from Google Drive.

`GET /`
Health check endpoint.
