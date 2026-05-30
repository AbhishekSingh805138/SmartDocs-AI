# API Reference

Base URL: `http://localhost:8000/api/v1`

## Endpoints

### Health Check

```
GET /api/v1/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "index_loaded": true,
  "documents_count": 150
}
```

### Upload PDF

```
POST /api/v1/upload
Content-Type: multipart/form-data
```

| Field | Type | Description |
|-------|------|-------------|
| file  | File | PDF file (max 50MB) |

Response:
```json
{
  "filename": "document.pdf",
  "pages": 25,
  "chunks": 87,
  "message": "Successfully processed document.pdf"
}
```

### List Documents

```
GET /api/v1/documents
```

Response:
```json
{
  "documents": [
    {"filename": "document.pdf", "size_mb": 2.34}
  ]
}
```

### Chat

```
POST /api/v1/chat
Content-Type: application/json
```

Request:
```json
{
  "question": "What is machine learning?",
  "top_k": 5
}
```

Response:
```json
{
  "answer": "Based on the uploaded documents...",
  "sources": ["document.pdf (p.12)", "document.pdf (p.15)"],
  "chunks_used": 5
}
```
