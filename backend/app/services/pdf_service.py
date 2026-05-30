import re
from pathlib import Path

import fitz  # PyMuPDF

from app.core.logger import logger


def extract_text_from_pdf(pdf_path: Path) -> list[dict]:
    """Extract text from each page of a PDF file.

    Returns a list of dicts with page_number and text content.
    """
    logger.info(f"Extracting text from: {pdf_path.name}")
    pages = []

    with fitz.open(str(pdf_path)) as doc:
        for page_num, page in enumerate(doc, start=1):
            raw_text = page.get_text("text")
            cleaned = _clean_text(raw_text)
            if cleaned.strip():
                pages.append({
                    "page_number": page_num,
                    "text": cleaned,
                    "source": pdf_path.name,
                })

    logger.info(f"Extracted {len(pages)} pages from {pdf_path.name}")
    return pages


def _clean_text(text: str) -> str:
    """Clean extracted text by normalizing whitespace and removing artifacts."""
    # Replace multiple newlines with single newline
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Replace multiple spaces with single space
    text = re.sub(r" {2,}", " ", text)
    # Remove null bytes and control characters (keep newlines and tabs)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    return text.strip()
