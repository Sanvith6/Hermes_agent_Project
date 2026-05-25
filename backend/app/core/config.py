from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import field_validator
from typing import Any

class Settings(BaseSettings):
    # App
    APP_NAME: str = "WhatsApp Clone"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/whatsapp"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: Any = ["http://localhost:3000", "http://localhost:8080"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> list:
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        raise ValueError(v)
    
    # MinIO
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "whatsapp-files"
    MINIO_URL: str = "http://localhost:9000"
    MINIO_SECURE: bool = False
    
    # Upload
    MAX_FILE_SIZE: int = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS: set = {"jpg", "jpeg", "png", "gif", "pdf", "doc", "docx", "mp3", "wav", "mp4"}
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
