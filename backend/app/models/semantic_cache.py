from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from pgvector.sqlalchemy import Vector

from app.database.connection  import Base

class SemanticCache(Base):
    __tablename__ = "semantic_cache"

    id = Column(Integer,primary_key=True, index=True)

    prompt = Column(String, nullable=False)

    prompt_hash = Column(String, unique=True, index=True, nullable=False)

    embedding = Column(Vector(1536), nullable=False)

    response = Column(Text, nullable=False)

    hit_count = Column(Integer,  default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
