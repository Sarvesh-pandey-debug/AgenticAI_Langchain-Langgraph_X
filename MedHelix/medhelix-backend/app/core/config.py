from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """
    MedHelix Application Settings
    All values loaded from .env file or environment variables
    """

    #App 
    APP_NAME: str = "MedHelix"
    APP_ENV: str = "development"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    #Database 
    DATABASE_URL: str              # async (asyncpg)
    DATABASE_URL_SYNC: str         # sync (psycopg2 — for Alembic)

    #Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_TTL_SECONDS: int = 3600

    #Auth0
    AUTH0_DOMAIN: str = ""
    AUTH0_CLIENT_ID: str = ""
    AUTH0_CLIENT_SECRET: str = ""
    AUTH0_AUDIENCE: str = "https://api.medhelix.com"
    AUTH0_ALGORITHMS: list[str] = ["RS256"]

    #AI / LLM 
    ANTHROPIC_API_KEY: str = ""
    CLAUDE_MODEL: str = "claude-3-5-sonnet-20241022"
    LLM_MAX_TOKENS: int = 4096
    LLM_TEMPERATURE: float = 0

    #AWS 
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: str = "medhelix-documents-dev"
    AWS_KMS_KEY_ID: str = ""

    # EHR 
    EPIC_CLIENT_ID: str = ""
    EPIC_CLIENT_SECRET: str = ""
    EPIC_BASE_URL: str = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4"
    EPIC_TOKEN_URL: str = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"

    ECW_API_KEY: str = ""
    ECW_BASE_URL: str = ""

    #Clearinghouse 
    STEDI_API_KEY: str = ""
    STEDI_BASE_URL: str = "https://healthcare.us.stedi.com/2024-04-01"

    #Pagination 
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    #HITL Thresholds 
    CODING_CONFIDENCE_THRESHOLD: float = 0.85
    AUTO_APPROVE_THRESHOLD: float = 0.95

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("AUTH0_ALGORITHMS", mode="before")
    @classmethod
    def parse_algorithms(cls, v):
        if isinstance(v, str):
            return [algo.strip() for algo in v.split(",")]
        return v

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance — only loads .env once"""
    return Settings()


# Shortcut for easy import
settings = get_settings()
