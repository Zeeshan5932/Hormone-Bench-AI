from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Centralized application configuration strictly managed by Pydantic."""

    # API Keys
    GOOGLE_API_KEY: str
    GROQ_API_KEY: str
    TAVILY_API_KEY: Optional[str] = None
    FIRECRAWL_API_KEY: Optional[str] = None
    NCBI_API_KEY: Optional[str] = None
    SEMANTIC_SCHOLAR_API_KEY: Optional[str] = None

    # Model Specifications
    LLM_MODEL: str = "GPT OSS 120B"
    EMBEDDING_MODEL: str = "gemini-embedding-001"
    MAX_TOKENS: int = 2048
    # Application Parameters
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Paths
    CHROMA_PERSIST_DIR: str = str(BASE_DIR / "data" / "chroma_db")
    DOCUMENTS_DIR: str = str(BASE_DIR / "data" / "documents")
    SESSIONS_DB_PATH: str = str(BASE_DIR / "data" / "sessions.sqlite3")
    KG_DB_PATH: str = str(BASE_DIR / "data" / "knowledge_graph.sqlite3")
    PROMPT_LIBRARY_DIR: str = str(BASE_DIR / "app" / "prompts" / "library")

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()