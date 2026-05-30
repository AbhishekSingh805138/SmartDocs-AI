from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.core.logger import logger


def chunk_pages(pages: list[dict]) -> list[dict]:
    """Split page texts into overlapping chunks for embedding.

    Each chunk retains metadata about its source file and page number.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = []
    for page in pages:
        page_chunks = splitter.split_text(page["text"])
        for i, chunk_text in enumerate(page_chunks):
            chunks.append({
                "text": chunk_text,
                "metadata": {
                    "source": page["source"],
                    "page": page["page_number"],
                    "chunk_index": i,
                },
            })

    logger.info(f"Created {len(chunks)} chunks from {len(pages)} pages")
    return chunks
