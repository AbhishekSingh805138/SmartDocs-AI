APP_NAME = "SmartDocs AI"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "RAG-powered personal assistant for PDF document Q&A"

# API
API_PREFIX = "/api/v1"

# Upload
ALLOWED_EXTENSIONS = {".pdf"}
MAX_FILE_SIZE_MB = 50

# Prompt template for RAG
RAG_SYSTEM_PROMPT = """You are SmartDocs AI, an intelligent assistant that answers questions based on the provided document context.

Instructions:
- Answer the question using ONLY the information from the provided context.
- If the context does not contain enough information to answer, say so clearly.
- Cite relevant details from the context to support your answer.
- Be concise but thorough in your response.
- Use bullet points or structured formatting when it improves clarity."""

RAG_USER_PROMPT_TEMPLATE = """Context from uploaded documents:
---
{context}
---

Question: {question}

Provide a detailed and accurate answer based on the context above."""
