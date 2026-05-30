from app.core.config import settings
from app.core.logger import logger
from app.services.vector_service import get_vector_store


def retrieve_relevant_chunks(query: str, top_k: int | None = None) -> list[dict]:
    """Retrieve the most relevant document chunks for a given query.

    Returns a list of dicts with 'text', 'metadata', and 'score' keys.
    """
    store = get_vector_store()
    if store is None:
        logger.warning("No vector store available for retrieval")
        return []

    k = top_k or settings.top_k
    results = store.similarity_search_with_score(query, k=k)

    chunks = []
    for doc, score in results:
        chunks.append({
            "text": doc.page_content,
            "metadata": doc.metadata,
            "score": float(score),
        })

    logger.info(f"Retrieved {len(chunks)} chunks for query: {query[:80]}...")
    return chunks
