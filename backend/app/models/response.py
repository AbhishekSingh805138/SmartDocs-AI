from pydantic import BaseModel
from typing import Optional


class UploadResponse(BaseModel):
    filename: str
    pages: int
    chunks: int
    message: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    chunks_used: int


class HealthResponse(BaseModel):
    status: str
    version: str
    index_loaded: bool
    documents_count: int


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
