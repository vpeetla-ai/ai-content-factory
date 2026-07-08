"""Public ops metrics — anonymized aggregates for portfolio / SLO dashboard."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.ops_metrics import collect_ops_metrics

router = APIRouter(prefix="/ops", tags=["Operations"])


@router.get("/metrics")
async def ops_metrics(db: Annotated[AsyncSession, Depends(get_db)]):
    """Anonymized pipeline metrics — no PII, safe for public landing page."""
    return await collect_ops_metrics(db)
