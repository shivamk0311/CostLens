from sqlalchemy import Column, String, Integer, Float, DateTime
from datetime import datetime
from app.database.connection import Base

class LLMEvent(Base):

    __tablename__ = "llm_events"

    id = Column(Integer, primary_key=True, index=True)

    feature = Column(String)

    model = Column(String)

    prompt_tokens = Column(Integer)

    completion_tokens = Column(Integer)

    total_tokens = Column(Integer)

    estimated_cost = Column(Float)

    latency_ms = Column(Integer)

    created_at = Column(
        DateTime,
        default = datetime.utcnow
    )