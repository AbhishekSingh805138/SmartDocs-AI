from langchain_openai import OpenAIEmbeddings

from app.core.config import settings
from app.core.logger import logger

_embeddings_instance: OpenAIEmbeddings | None = None


def get_embeddings() -> OpenAIEmbeddings:
    """Get or create the singleton OpenAI embeddings instance."""
    global _embeddings_instance
    if _embeddings_instance is None:
        _embeddings_instance = OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openai_api_key,
        )
        logger.info(f"Initialized embeddings model: {settings.embedding_model}")
    return _embeddings_instance


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a list of texts."""
    embeddings = get_embeddings()
    logger.info(f"Generating embeddings for {len(texts)} texts")
    return embeddings.embed_documents(texts)


def embed_query(query: str) -> list[float]:
    """Generate embedding for a single query string."""
    embeddings = get_embeddings()
    return embeddings.embed_query(query)
