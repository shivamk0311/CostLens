from pydantic import BaseModel
from datetime import datetime

class LLMEventCreate(BaseModel):
    feature: str | None = None
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost: float
    latency_ms: float
    cache_hit: bool = False
    cache_type: str | None = None
    created_at: datetime