import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.core.config import settings
from app.core.constants import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB
from app.core.logger import logger
from app.models.response import UploadResponse
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_service import chunk_pages
from app.services.vector_service import add_chunks_to_store

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF file, extract text, chunk it, and store embeddings."""
    # Validate file extension
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Only PDF files are allowed. Got: {suffix}",
        )

    # Validate file size
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large ({size_mb:.1f}MB). Max: {MAX_FILE_SIZE_MB}MB",
        )

    # Save uploaded file
    upload_dir = settings.pdf_upload_dir
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / file.filename

    with open(file_path, "wb") as f:
        f.write(contents)

    logger.info(f"Saved uploaded file: {file.filename} ({size_mb:.1f}MB)")

    try:
        # Extract text
        pages = extract_text_from_pdf(file_path)
        if not pages:
            raise HTTPException(
                status_code=400,
                detail="Could not extract any text from the PDF.",
            )

        # Chunk text
        chunks = chunk_pages(pages)

        # Store embeddings
        add_chunks_to_store(chunks)

        return UploadResponse(
            filename=file.filename,
            pages=len(pages),
            chunks=len(chunks),
            message=f"Successfully processed {file.filename}",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing {file.filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@router.get("/documents")
async def list_documents():
    """List all uploaded PDF documents."""
    upload_dir = settings.pdf_upload_dir
    if not upload_dir.exists():
        return {"documents": []}

    docs = []
    for f in sorted(upload_dir.iterdir()):
        if f.suffix.lower() == ".pdf":
            docs.append({
                "filename": f.name,
                "size_mb": round(f.stat().st_size / (1024 * 1024), 2),
            })

    return {"documents": docs}
