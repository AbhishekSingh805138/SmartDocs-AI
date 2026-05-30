# Architecture

## Overview

SmartDocs AI is a RAG (Retrieval-Augmented Generation) pipeline that enables Q&A over uploaded PDF documents.

## Components

### Backend (FastAPI)

- **API Layer** (`app/api/`) — REST endpoints for upload, chat, and health check
- **Services Layer** (`app/services/`) — Business logic for PDF parsing, chunking, embedding, vector storage, retrieval, and LLM generation
- **Core** (`app/core/`) — Configuration, constants, and logging
- **Models** (`app/models/`) — Pydantic request/response schemas

### Frontend (Streamlit)

- **Upload Page** — PDF file upload and processing
- **Chat Page** — Conversational Q&A interface with source citations

### Data Flow

```
PDF Upload → PyMuPDF (text extraction) → Text Cleaning → Recursive Chunking
→ OpenAI Embeddings (text-embedding-3-small) → FAISS Vector Store (local)

User Question → Query Embedding → FAISS Similarity Search (top-k=5)
→ Context Assembly → GPT-4o → Answer with Sources
```

### Storage

- **FAISS Index** — Local vector database stored in `backend/data/faiss_index/`
- **PDFs** — Uploaded files stored in `backend/data/pdfs/`
- **Processed** — Intermediate data in `backend/data/processed/`
