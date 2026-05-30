# Setup Guide

## Prerequisites

- Python 3.11+
- OpenAI API key

## Installation

### 1. Clone and navigate to the project

```bash
cd "SmartDocs AI"
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure environment

Edit `backend/.env` and set your OpenAI API key:

```
OPENAI_API_KEY=sk-your-key-here
```

## Running

### Start the backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

The API docs will be available at `http://localhost:8000/docs`

### Start the frontend

In a separate terminal:

```bash
cd frontend
streamlit run app.py
```

The UI will open at `http://localhost:8501`

## Docker

```bash
cd docker
docker-compose up --build
```

## Utility Scripts

```bash
# Index all PDFs in data/pdfs/
python scripts/create_index.py

# Delete and rebuild the index
python scripts/reindex.py

# Clean all data files
python scripts/cleanup.py
```
