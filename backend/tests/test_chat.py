from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch("app.api.chat.get_vector_store", return_value=None)
def test_chat_no_documents(mock_store):
    response = client.post(
        "/api/v1/chat",
        json={"question": "What is AI?"},
    )
    assert response.status_code == 400
    assert "No documents" in response.json()["detail"]


@patch("app.api.chat.generate_answer", return_value="AI is artificial intelligence.")
@patch("app.api.chat.retrieve_relevant_chunks")
@patch("app.api.chat.get_vector_store")
def test_chat_success(mock_store, mock_retrieve, mock_generate):
    mock_store.return_value = MagicMock()
    mock_retrieve.return_value = [
        {
            "text": "AI stands for artificial intelligence",
            "metadata": {"source": "intro.pdf", "page": 1},
            "score": 0.85,
        }
    ]

    response = client.post(
        "/api/v1/chat",
        json={"question": "What is AI?", "top_k": 3},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "AI is artificial intelligence."
    assert len(data["sources"]) > 0
    assert data["chunks_used"] == 1


def test_chat_empty_question():
    response = client.post(
        "/api/v1/chat",
        json={"question": ""},
    )
    assert response.status_code == 422  # Validation error
