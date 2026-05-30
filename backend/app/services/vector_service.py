import json
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.core.config import settings
from app.core.logger import logger
from app.services.embedding_service import get_embeddings

_vector_store: FAISS | None = None


def get_vector_store() -> FAISS | None:
    """Get the current FAISS vector store, loading from disk if needed."""
    global _vector_store
    if _vector_store is None:
        _vector_store = load_index()
    return _vector_store


def add_chunks_to_store(chunks: list[dict]) -> FAISS:
    """Add document chunks to the FAISS vector store and persist to disk."""
    global _vector_store

    documents = [
        Document(page_content=chunk["text"], metadata=chunk["metadata"])
        for chunk in chunks
    ]

    embeddings = get_embeddings()

    if _vector_store is None:
        _vector_store = FAISS.from_documents(documents, embeddings)
        logger.info(f"Created new FAISS index with {len(documents)} documents")
    else:
        _vector_store.add_documents(documents)
        logger.info(f"Added {len(documents)} documents to existing FAISS index")

    save_index(_vector_store)
    return _vector_store


def save_index(store: FAISS) -> None:
    """Save the FAISS index to disk."""
    index_dir = settings.faiss_index_dir
    index_dir.mkdir(parents=True, exist_ok=True)
    store.save_local(str(index_dir))
    logger.info(f"FAISS index saved to {index_dir}")


def load_index() -> FAISS | None:
    """Load a FAISS index from disk if it exists."""
    index_dir = settings.faiss_index_dir
    index_file = index_dir / "index.faiss"

    if not index_file.exists():
        logger.info("No existing FAISS index found")
        return None

    embeddings = get_embeddings()
    store = FAISS.load_local(
        str(index_dir), embeddings, allow_dangerous_deserialization=True
    )
    logger.info("FAISS index loaded from disk")
    return store


def get_index_stats() -> dict:
    """Get statistics about the current vector store."""
    store = get_vector_store()
    if store is None:
        return {"loaded": False, "documents_count": 0}

    return {
        "loaded": True,
        "documents_count": store.index.ntotal,
    }


def delete_index() -> None:
    """Delete the FAISS index from disk and clear memory."""
    global _vector_store
    _vector_store = None

    index_dir = settings.faiss_index_dir
    for f in index_dir.iterdir():
        if f.name != ".gitkeep":
            f.unlink()
    logger.info("FAISS index deleted")
