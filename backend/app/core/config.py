"""Environment-aware application configuration (local vs production)."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parents[3]


def _env_files() -> tuple[str, ...]:
    files: list[str] = []
    for name in (".env", ".env.local"):
        path = _PROJECT_ROOT / name
        if path.exists():
            files.append(str(path))
    return tuple(files)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_env_files(),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Environment ──────────────────────────────────────
    app_env: Literal["development", "production", "test"] = "development"
    app_name: str = "ai-content-factory"
    mock_llm: bool = True
    app_secret_key: str = "dev-secret-change-me"
    api_base_url: str = "http://localhost:8000/api/v1"
    frontend_url: str = "http://localhost:3000"
    cors_origins: str = ""  # comma-separated; defaults to frontend_url

    # ── Database ─────────────────────────────────────────
    database_url: str = "postgresql+asyncpg://acf:acf@localhost:5432/ai_content_factory"

    # ── Redis ────────────────────────────────────────────
    redis_url: str = "redis://localhost:6379/0"

    # ── Auth (Clerk + JWT) ───────────────────────────────
    clerk_secret_key: str = ""
    clerk_publishable_key: str = ""
    clerk_jwks_url: str = ""
    allow_dev_auth: bool = True  # local dev token bypass when Clerk not configured
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # ── LLM Providers ────────────────────────────────────
    google_api_key: str = ""
    groq_api_key: str = ""
    cerebras_api_key: str = ""
    anthropic_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"
    litellm_proxy_url: str = "http://localhost:4000"
    litellm_master_key: str = "sk-acf-dev"
    use_litellm_proxy: bool = False

    # ── Vector DB ────────────────────────────────────────
    vector_backend: Literal["qdrant", "pinecone", "none"] = "qdrant"
    pinecone_api_key: str = ""
    pinecone_index: str = "acf-research"
    pinecone_environment: str = "us-east-1"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection: str = "acf_research"
    embedding_model: str = "text-embedding-004"
    embedding_dimensions: int = 768

    # ── Object Storage (Cloudflare R2) ───────────────────
    r2_account_id: str = ""
    r2_access_key_id: str = ""
    r2_secret_access_key: str = ""
    r2_bucket_name: str = "acf-media"
    r2_public_url: str = ""

    # ── Observability ────────────────────────────────────
    langsmith_api_key: str = ""
    langsmith_project: str = "ai-content-factory"
    langsmith_tracing: bool = True
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = "https://cloud.langfuse.com"
    langfuse_enabled: bool = True
    sentry_dsn: str = ""
    sentry_traces_sample_rate: float = 0.2
    otel_exporter_otlp_endpoint: str = ""
    log_level: str = "INFO"
    log_json: bool = False

    # ── Platform OAuth (publish targets) ─────────────────
    linkedin_client_id: str = ""
    linkedin_client_secret: str = ""
    medium_integration_token: str = ""
    x_api_key: str = ""
    x_api_secret: str = ""
    x_access_token: str = ""
    x_access_token_secret: str = ""

    # ── Redis TTLs (seconds) ─────────────────────────────
    pipeline_state_ttl: int = 86400
    research_cache_ttl: int = 21600
    session_ttl: int = 604800

    # ── Production ops ───────────────────────────────────
    run_migrations_on_startup: bool = False
    port: int = 8000
    workers: int = 2

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, v: str) -> str:
        # Render/Heroku provide postgres:// — asyncpg needs postgresql+asyncpg://
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+asyncpg://", 1)
        if v.startswith("postgresql://") and "+asyncpg" not in v:
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    @model_validator(mode="after")
    def production_defaults(self) -> "Settings":
        if self.is_production:
            self.allow_dev_auth = False
            self.mock_llm = False
            self.log_json = True
            self.run_migrations_on_startup = True
            if self.app_secret_key == "dev-secret-change-me":
                raise ValueError("APP_SECRET_KEY must be set in production")
        return self

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"

    @property
    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip():
            return [o.strip() for o in self.cors_origins.split(",") if o.strip()]
        return [self.frontend_url, "http://localhost:3000"]

    @property
    def clerk_configured(self) -> bool:
        return bool(self.clerk_secret_key and self.clerk_jwks_url)

    @property
    def langsmith_enabled(self) -> bool:
        return bool(self.langsmith_api_key and self.langsmith_tracing)

    @property
    def langfuse_configured(self) -> bool:
        return bool(
            self.langfuse_enabled
            and self.langfuse_public_key
            and self.langfuse_secret_key
        )

    @property
    def vector_enabled(self) -> bool:
        if self.vector_backend == "none":
            return False
        if self.vector_backend == "pinecone":
            return bool(self.pinecone_api_key)
        return bool(self.qdrant_url)

    @property
    def sync_database_url(self) -> str:
        url = self.database_url
        return url.replace("+asyncpg", "+psycopg2").replace("postgresql+psycopg2", "postgresql+psycopg2")


@lru_cache
def get_settings() -> Settings:
    return Settings()
