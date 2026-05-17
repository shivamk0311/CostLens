import time
from fastapi import APIRouter, Header, Depends
from sqlalchemy.orm import Session

from app.schemas.chat import ChatCompletionRequest
from app.dependencies.db import get_db
from app.services.openai_service import call_openai_chat_completion
from app.services.cost_service import calculate_cost
from app.repositories.event_repository import create_llm_event

router = APIRouter()

@router.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest, db: Session=Depends(get_db), x_costlens_feature: str | None = Header(default = "unknown")):
    
    start_time = time.time()
    openai_response = call_openai_chat_completion(request.model_dump())

    end_time = time.time()
    latency_ms = round((end_time - start_time)*1000)

    usage = openai_response.get("usage",{})

    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)

    estimated_cost = calculate_cost(request.model, prompt_tokens, completion_tokens)

    create_llm_event(
        db=db,
        feature=x_costlens_feature,
        model=request.model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        estimated_cost=estimated_cost,
        latency_ms=latency_ms
    )

    return {
        "costlens":{
            "feature":x_costlens_feature,
            "latency_ms":latency_ms,
            "model": request.model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "estimated_cost_usd": estimated_cost,
        },
        "openai_response": openai_response
    }

    
        