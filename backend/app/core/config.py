from pathlib import Path
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application
    APP_NAME: str = "VidMind"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"

    # Storage & DB
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/vidmind.db"
    DATA_DIRECTORY: str = "./data"

    # Hardware & Performance
    HARDWARE_PROFILE: str = "auto"
    MAX_CONCURRENT_JOBS: int = 2

    # Transcription (faster-whisper)
    TRANSCRIPTION_MODEL: str = "base"
    TRANSCRIPTION_DEVICE: str = "cpu"
    TRANSCRIPTION_COMPUTE_TYPE: str = "int8"
    TRANSCRIPTION_CPU_THREADS: int = 3
    TRANSCRIPTION_BEAM_SIZE: int = 5
    TRANSCRIPTION_VAD_FILTER: bool = True

    # Local LLM (Ollama)
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "llama3.2:1b"
    LLM_PROVIDER: str = "ollama"
    LLM_TIMEOUT_SECONDS: int = 120
    LLM_TEMPERATURE: float = 0.2

    # Embeddings & RAG
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DEVICE: str = "cpu"
    VECTOR_INDEX_TYPE: str = "faiss"
    TOP_K_RETRIEVAL: int = 5

    # Semantic Chunking
    CHUNK_TARGET_MINUTES: int = 10
    CHUNK_MIN_MINUTES: int = 5
    CHUNK_MAX_MINUTES: int = 15

    # Vision & OCR
    ENABLE_VISION: bool = False
    ENABLE_OCR: bool = False
    VISION_MODEL: str = "llava:7b"
    FRAME_INTERVAL_SECONDS: int = 30
    OCR_ENGINE: str = "tesseract"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def data_path(self) -> Path:
        p = Path(self.DATA_DIRECTORY)
        p.mkdir(parents=True, exist_ok=True)
        return p


settings = Settings()
