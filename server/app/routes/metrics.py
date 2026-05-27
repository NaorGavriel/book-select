from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import redis as redis_lib

from app.core.redis_client import get_redis_client
from app.db import get_db
from app.schemas.metrics import MetricsResponse
from app.services.auth import get_current_admin_user
from app.services.metrics import get_all_metrics

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("", response_model=MetricsResponse)
def read_metrics(
    db: Session = Depends(get_db),
    rc: redis_lib.Redis = Depends(get_redis_client),
    _: object = Depends(get_current_admin_user),
):
    """Return a full system metrics snapshot. Requires admin privileges."""
    return get_all_metrics(db=db, rc=rc)
