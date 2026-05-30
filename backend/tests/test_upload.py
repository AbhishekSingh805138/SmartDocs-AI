import io
from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_rejects_non_pdf():
    file = io.BytesIO(b"not a pdf")
    response = client.post(
        "/api/v1/upload",
        files={"file": ("test.txt", file, "text/plain")},
    )
    assert response.status_code == 400
    assert "Only PDF files" in response.json()["detail"]


def test_upload_rejects_oversized_file():
    # Create a file larger than 50MB
    file = io.BytesIO(b"0" * (51 * 1024 * 1024))
    response = client.post(
        "/api/v1/upload",
        files={"file": ("big.pdf", file, "application/pdf")},
    )
    assert response.status_code == 400
    assert "too large" in response.json()["detail"]


@patch("app.api.upload.add_chunks_to_store")
@patch("app.api.upload.chunk_pages")
@patch("app.api.upload.extract_text_from_pdf")
def test_upload_success(mock_extract, mock_chunk, mock_store):
    mock_extract.return_value = [
        {"page_number": 1, "text": "Hello world", "source": "test.pdf"}
    ]
    mock_chunk.return_value = [
        {"text": "Hello world", "metadata": {"source": "test.pdf", "page": 1, "chunk_index": 0}}
    ]
    mock_store.return_value = MagicMock()

    # Minimal valid PDF bytes
    pdf_bytes = b"%PDF-1.4 minimal"
    response = client.post(
        "/api/v1/upload",
        files={"file": ("test.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.pdf"
    assert data["pages"] == 1
    assert data["chunks"] == 1


def test_list_documents():
    response = client.get("/api/v1/documents")
    assert response.status_code == 200
    assert "documents" in response.json()
