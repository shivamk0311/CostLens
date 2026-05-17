from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.repositories.event_repository import get_cost_summary

router = APIRouter()

@router.get('/cost/summary')
def costs_summary(db: Session=Depends(get_db)):
    return get_cost_summary(db)