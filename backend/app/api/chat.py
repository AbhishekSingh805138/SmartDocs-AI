from fastapi import APIRouter, HTTPException

from app.core.logger import logger
from app.models.request import ChatRequest
from app.models.response import ChatResponse
from app.services.retrieval_service import retrieve_relevant_chunks
from app.services.llm_service import generate_answer
from app.services.vector_service import get_vector_store

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Answer a question using context retrieved from uploaded documents."""
    store = get_vector_store()
    if store is None:
        raise HTTPException(
            status_code=400,
            detail="No documents have been uploaded yet. Please upload a PDF first.",
        )

    try:
        # Retrieve relevant chunks
        chunks = retrieve_relevant_chunks(request.question, top_k=request.top_k)

        # Generate answer
        answer = generate_answer(request.question, chunks)

        # Collect unique sources
        sources = list({
            f"{c['metadata'].get('source', 'Unknown')} (p.{c['metadata'].get('page', '?')})"
            for c in chunks
        })

        return ChatResponse(
            answer=answer,
            sources=sorted(sources),
            chunks_used=len(chunks),
        )

    except Exception as e:
        logger.error(f"Error during chat: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")
