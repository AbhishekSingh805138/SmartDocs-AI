from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.config import settings
from app.core.constants import RAG_SYSTEM_PROMPT, RAG_USER_PROMPT_TEMPLATE
from app.core.logger import logger

_llm_instance: ChatOpenAI | None = None


def get_llm() -> ChatOpenAI:
    """Get or create the singleton LLM instance."""
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = ChatOpenAI(
            model=settings.llm_model,
            openai_api_key=settings.openai_api_key,
            temperature=0.3,
            max_tokens=2000,
        )
        logger.info(f"Initialized LLM: {settings.llm_model}")
    return _llm_instance


def generate_answer(question: str, context_chunks: list[dict]) -> str:
    """Generate an answer using retrieved context chunks and the LLM."""
    if not context_chunks:
        return (
            "I don't have any relevant information in the uploaded documents "
            "to answer your question. Please upload relevant PDF documents first."
        )

    context = _build_context(context_chunks)

    user_prompt = RAG_USER_PROMPT_TEMPLATE.format(
        context=context,
        question=question,
    )

    llm = get_llm()
    messages = [
        SystemMessage(content=RAG_SYSTEM_PROMPT),
        HumanMessage(content=user_prompt),
    ]

    logger.info(f"Sending query to LLM with {len(context_chunks)} context chunks")
    response = llm.invoke(messages)
    return response.content


def _build_context(chunks: list[dict]) -> str:
    """Build a formatted context string from retrieved chunks."""
    parts = []
    for i, chunk in enumerate(chunks, start=1):
        source = chunk["metadata"].get("source", "Unknown")
        page = chunk["metadata"].get("page", "?")
        parts.append(f"[Source: {source}, Page {page}]\n{chunk['text']}")
    return "\n\n---\n\n".join(parts)
