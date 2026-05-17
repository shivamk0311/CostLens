from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.repositories.event_repository import get_recent_events

router = APIRouter()


@router.get("/events")
def get_events(db: Session = Depends(get_db)):
    return get_recent_events(db)