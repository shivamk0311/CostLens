from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.repositories.semantic_cache_repository import get_cache_stats

router = APIRouter()


@router.get("/cache/stats")
def cache_stats(db: Session = Depends(get_db)):
    return get_cache_stats(db)