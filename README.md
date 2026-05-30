# SmartDocs AI

RAG-powered personal assistant for PDF document Q&A.

Upload PDF documents, extract and store their knowledge, then ask questions and get accurate answers grounded in your documents.

## Tech Stack

| Component    | Technology                |
|-------------|---------------------------|
| Frontend    | Streamlit                 |
| Backend     | FastAPI                   |
| PDF Parser  | PyMuPDF                   |
| Chunking    | RecursiveCharacterTextSplitter |
| Embeddings  | text-embedding-3-small    |
| Vector DB   | FAISS (local)             |
| LLM         | GPT-4o                    |
| Framework   | LangChain                 |

## Quick Start

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Set your OpenAI API key
# Edit backend/.env → OPENAI_API_KEY=sk-your-key-here

# Start backend
cd backend
uvicorn app.main:app --reload --port 8000

# Start frontend (separate terminal)
cd frontend
streamlit run app.py
```

## Project Structure

```
backend/          FastAPI backend with RAG pipeline services
frontend/         Streamlit UI for upload and chat
scripts/          Utility scripts for indexing and cleanup
docker/           Docker and docker-compose configs
docs/             Architecture, API, and setup documentation
```

## Documentation

- [Architecture](docs/architecture.md)
- [API Reference](docs/api.md)
- [Setup Guide](docs/setup.md)

## License

MIT
