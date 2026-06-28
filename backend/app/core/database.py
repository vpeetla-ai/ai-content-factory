"""Database session management."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

settings = get_settings()


def _asyncpg_connect_args(database_url: str) -> dict:
    """Neon and other managed Postgres require TLS for asyncpg."""
    if any(
        marker in database_url
        for marker in ("ssl=require", "sslmode=require", "neon.tech", ".render.com")
    ):
        return {"ssl": True}
    return {}


engine = create_async_engine(
    settings.database_url,
    echo=settings.app_env == "development",
    connect_args=_asyncpg_connect_args(settings.database_url),
)
async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
