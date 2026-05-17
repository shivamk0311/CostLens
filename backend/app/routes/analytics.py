from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.repositories.event_repository import get_cost_summary, get_cost_by_feature, get_cost_by_model

router = APIRouter()

@router.get('/cost/summary')
def costs_summary(db: Session=Depends(get_db)):
    return get_cost_summary(db)

@router.get("/cost/by-feature")
def costs_by_feature(db : Session=Depends(get_db)):
    return get_cost_by_feature(db)

@router.get("/costs/by-model")
def costs_by_model (db : Session=Depends(get_db)):
    return get_cost_by_model(db)
    