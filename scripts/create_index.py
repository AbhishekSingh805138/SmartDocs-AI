"""Create FAISS index from all PDFs in the data/pdfs directory."""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.core.config import settings
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_service import chunk_pages
from app.services.vector_service import add_chunks_to_store


def main():
    pdf_dir = settings.pdf_upload_dir
    if not pdf_dir.exists():
        print(f"PDF directory not found: {pdf_dir}")
        return

    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found.")
        return

    print(f"Found {len(pdf_files)} PDF file(s)")

    total_chunks = 0
    for pdf_path in pdf_files:
        print(f"\nProcessing: {pdf_path.name}")
        pages = extract_text_from_pdf(pdf_path)
        chunks = chunk_pages(pages)
        add_chunks_to_store(chunks)
        total_chunks += len(chunks)
        print(f"  Pages: {len(pages)}, Chunks: {len(chunks)}")

    print(f"\nDone. Total chunks indexed: {total_chunks}")


if __name__ == "__main__":
    main()
