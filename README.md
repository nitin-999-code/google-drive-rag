# Google Drive RAG System

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-000000?style=for-the-badge)
![SentenceTransformers](https://img.shields.io/badge/SentenceTransformers-FF9D00?style=for-the-badge)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

## Overview

This project implements a production-ready Retrieval-Augmented Generation (RAG) system that seamlessly integrates with Google Drive. It connects to a designated Drive folder, retrieves documents, processes them into meaningful chunks, generates embeddings using `SentenceTransformers`, and stores them in an efficient `FAISS` vector database. It then enables users to ask questions and receive semantically relevant answers based on the indexed documents.

RAG is utilized to overcome the context limits of traditional LLMs by providing precise, dynamically fetched context derived directly from private knowledge bases. The system is fully containerized with Docker, highly scalable, and deployed on the cloud using Render, ensuring reliable production readiness.

## Features

- **Google Drive Integration**: Automatically pull and sync files via the Google Drive API.
- **Document Ingestion**: Seamless handling of multiple documents.
- **PDF and Text Parsing**: Built-in support for extracting content from `.pdf` and `.txt` files.
- **Text Chunking**: Intelligent splitting of large documents into processable segments.
- **Embedding Generation**: Utilizes `all-MiniLM-L6-v2` for high-quality sentence embeddings.
- **Vector Search using FAISS**: Extremely fast similarity search using in-memory FAISS indexing.
- **Semantic Question Answering**: Retrieves the most relevant chunks based on user queries.
- **REST API Endpoints**: Easy-to-use FastAPI layer for syncing and asking questions.
- **Docker Deployment**: Clean, minimal Dockerfile for consistent environments.
- **Cloud Hosting on Render**: Live and continuously accessible API deployment.

## System Architecture

```text
Google Drive
    ↓
File Fetching
    ↓
Text Extraction
    ↓
Chunking
    ↓
Embedding Model
    ↓
FAISS Vector Store
    ↓
Similarity Search
    ↓
Answer Generation
```

## Tech Stack

- **Python**: Core programming language.
- **FastAPI**: High-performance web framework for the APIs.
- **SentenceTransformers**: Generating dense vector embeddings.
- **FAISS**: Library for efficient similarity search and clustering of dense vectors.
- **Google Drive API**: External storage connector.
- **NumPy**: Matrix and array processing.
- **Docker**: Containerization.
- **Render**: Cloud PaaS hosting provider.

## Project Structure

```text
google-drive-rag/
│
├── api/
│   ├── main.py
│   └── rag_service.py
│
├── connectors/
│   └── gdrive.py
│
├── processing/
│   ├── parser.py
│   └── chunker.py
│
├── search/
│   └── vector_store.py
│
├── data/
│
├── Dockerfile
├── requirements.txt
└── README.md
```

## How the System Works

1. **Connect to Google Drive**: Authenticates via a Service Account to securely access private folders.
2. **Fetch files**: Identifies `.pdf` and `.txt` files.
3. **Extract text**: Uses `pypdf` and standard file parsing to grab all text content.
4. **Split into chunks**: Divides the text into overlapping segments (e.g., 500 characters) to preserve context while fitting embedding token limits.
5. **Generate embeddings**: Converts the text chunks into mathematical vector representations using `SentenceTransformers`.
6. **Store in FAISS**: Indexes the embeddings in FAISS, linking each vector to its source document and chunk text.
7. **Search relevant chunks**: When a query is made, it is embedded and compared against the FAISS index to find the most semantically similar context.
8. **Return answer**: The best chunks and their original source file names are returned to the user.

## API Endpoints

### `POST /sync-drive`

**Description:**  
Fetch and process files from Google Drive. Can be forced to clear cache and re-index using `?force_reindex=true`.

**Example request:**  
```http
POST /sync-drive
```

**Response:**
```json
{
  "status": "success",
  "processed_files": 3,
  "total_files": 3
}
```

### `POST /ask`

**Description:**  
Ask a question based on the previously indexed documents.

**Example request:**
```json
{
  "query": "What company is mentioned in the assignment document?"
}
```

**Response:**
```json
{
  "answer": "Based on the following context:\n\n...",
  "sources": ["document.pdf"]
}
```

## Installation (Local Setup)

```bash
git clone https://github.com/nitin-999-code/google-drive-rag.git
cd google-drive-rag
pip install -r requirements.txt
uvicorn api.main:app --reload
```
*Note: Make sure to place your `service_account.json` in the project root.*

## Docker Setup

```bash
# Build the Docker image
docker build -t gdrive-rag .

# Run the container
docker run -p 8000:8000 gdrive-rag
```

## Deployment

The system is deployed using a Docker container strategy on **Render**. 
- **Docker container**: Ensures the environment matches local development perfectly and handles system-level dependencies.
- **Render deployment**: Automatically builds the container and deploys the web service.
- **Auto scaling**: Render can scale the container based on demand.
- **Public API endpoint**: Accessible globally at `https://google-drive-rag-8b95.onrender.com/docs`.

## Environment Variables

Ensure the following are configured in your deployment environment:

- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your `service_account.json` file.
- `PORT`: The port your web server binds to (default: 8000).

## Example Workflow

1. **User uploads files to Google Drive** (e.g., training manuals, assignments).
2. **User calls `/sync-drive`** to pull down the newly added PDFs and TXT files.
3. **User asks question** via the `/ask` endpoint, probing for specifics within those documents.
4. **System returns answer** formatted with precise text chunks and source document citations.

## Screenshots Section

*(Placeholders for future media)*
- [Swagger UI]
- [Deployment logs]
- [Google Drive folder]
- [API response]

## Performance Notes

- **Lightweight embedding model**: `all-MiniLM-L6-v2` offers an excellent balance between speed and accuracy without demanding GPUs.
- **Fast semantic search**: FAISS executes similarity lookups in milliseconds, even across thousands of chunks.
- **Scalable architecture**: Decoupled processing layers allow seamless future upgrades to vector databases or embedding models.

## Future Improvements

- **Hybrid search**: Combining keyword (BM25) and semantic search for better accuracy.
- **Streaming responses**: Streaming tokens back to the client using WebSockets or Server-Sent Events.
- **Multi-user authentication**: Secure endpoints via OAuth2/JWT.
- **Vector database migration**: Upgrading from in-memory FAISS to Pinecone or Qdrant for persistent scale.
- **Caching layer**: Redis caching for repeated user queries.

## Author

**Nitin Sahu**  
*AI / Backend Developer*

## License

MIT License
