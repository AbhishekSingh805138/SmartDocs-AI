from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o"

    # Chunking
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Retrieval
    top_k: int = 5

    # Paths (relative to backend/)
    faiss_index_path: str = "data/faiss_index"
    pdf_upload_path: str = "data/pdfs"
    processed_path: str = "data/processed"

    # Logging
    log_level: str = "INFO"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    @property
    def faiss_index_dir(self) -> Path:
        return Path(self.faiss_index_path)

    @property
    def pdf_upload_dir(self) -> Path:
        return Path(self.pdf_upload_path)

    @property
    def processed_dir(self) -> Path:
        return Path(self.processed_path)


settings = Settings()
