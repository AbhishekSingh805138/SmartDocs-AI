from fastapi import APIRouter

from app.core.constants import APP_VERSION
from app.models.response import HealthResponse
from app.services.vector_service import get_index_stats

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API health and index status."""
    stats = get_index_stats()
    return HealthResponse(
        status="healthy",
        version=APP_VERSION,
        index_loaded=stats["loaded"],
        documents_count=stats["documents_count"],
    )
