"""AI Content Factory — application configuration."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    app_secret_key: str = "dev-secret-change-me"
    api_base_url: str = "http://localhost:8000/api/v1"
    frontend_url: str = "http://localhost:3000"

    database_url: str = "postgresql+asyncpg://acf:acf@localhost:5432/ai_content_factory"
    redis_url: str = "redis://localhost:6379/0"

    clerk_secret_key: str = ""
    clerk_publishable_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    google_api_key: str = ""
    groq_api_key: str = ""
    cerebras_api_key: str = ""
    anthropic_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"
    litellm_proxy_url: str = "http://localhost:4000"

    pinecone_api_key: str = ""
    pinecone_index: str = "acf-research"
    qdrant_url: str = "http://localhost:6333"

    langsmith_api_key: str = ""
    langsmith_project: str = "ai-content-factory"
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = "https://cloud.langfuse.com"
    sentry_dsn: str = ""

    # Redis TTLs (seconds)
    pipeline_state_ttl: int = 86400  # 24h
    research_cache_ttl: int = 21600  # 6h
    session_ttl: int = 604800  # 7d


@lru_cache
def get_settings() -> Settings:
    return Settings()
