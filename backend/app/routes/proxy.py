import time, json
from fastapi import APIRouter, Header, Depends
from sqlalchemy.orm import Session

from app.schemas.chat import ChatCompletionRequest
from app.dependencies.db import get_db
from app.services.openai_service import call_openai_chat_completion
from app.services.cost_service import calculate_cost
from app.repositories.event_repository import create_llm_event


from app.services.embedding_service import generate_embedding
from app.repositories.semantic_cache_repository import (
    find_exact_cache_match,
    store_cache_entry,
    increment_cache_hit,
    find_semantic_cache_match,
)

from app.services.mlflow_service import log_cache_experiment

router = APIRouter()

@router.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest, db: Session=Depends(get_db), x_costlens_feature: str | None = Header(default = "unknown")):
    
    start_time = time.time()
    prompt = "".join(message.content for message in request.messages)

    exact_cache_match = find_exact_cache_match(db, prompt)

    if exact_cache_match:
        increment_cache_hit(db, exact_cache_match)

        cached_response = json.loads(exact_cache_match.response)
        return {
            "costlens":{
                "cache_hit": True,
                "cache_type": "exact",
                "feature":x_costlens_feature,
                "model": request.model,
            },
            "openai_response": cached_response
        }
    
    embedding = generate_embedding(prompt)
    semantic_cache_match, similarity_score  =  (find_semantic_cache_match(db, embedding, similarity_threshold=0.90))

    if semantic_cache_match:
        increment_cache_hit(db, semantic_cache_match)
        cached_response = json.loads(semantic_cache_match.response)

        log_cache_experiment(
            threshold=0.80,
            similarity_score=similarity_score,
            cache_hit=True,
            latency_ms=0,
            estimated_cost=0,
        )

        return {
            "costlens": {
                "semantic_cache_hit": True,
                "cache-type": "semantic",
                "feature": x_costlens_feature,
                "model": request.model, 
            },
            "openai_response" : cached_response
        }

    openai_response = await call_openai_chat_completion(request.model_dump())

    end_time = time.time()
    latency_ms = round((end_time - start_time)*1000)

    usage = openai_response.get("usage",{})

    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)

    estimated_cost = calculate_cost(request.model, prompt_tokens, completion_tokens)

    store_cache_entry(
        db=db,
        prompt=prompt,
        embedding=embedding,
        response=json.dumps(openai_response),
    )

    log_cache_experiment(
        threshold=0.80,
        similarity_score=similarity_score,
        cache_hit=False,
        latency_ms=latency_ms,
        estimated_cost=estimated_cost,
    )

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
            "cache_hit": False,
            "cache_type": None,
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

    
        