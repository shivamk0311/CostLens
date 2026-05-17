from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
import httpx
import os, time

from app.database import engine, SessionLocal
from app.models import Base, LLMEvent

from sqlalchemy.orm import Session

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


app = FastAPI(
    title="CostLens API",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)

class Message(BaseModel):
    role: str 
    content: str 

class ChatCompletionRequest(BaseModel):
    model: str 
    messages: List[Message]
    temperature: Optional[float] = 0.7

def calculate_cost(model, prompt_tokens, completion_tokens):
    pricing = {
        "gpt-4o-mini" : {
            "input" : 0.15 /1_000_000,
            "output": 0.60 /1_000_000
        },
        "gpt-4o" : {
            "input" : 2.50 /1_000_000,
            "output": 10.00 /1_000_000
        },
    }

    model_pricing = pricing[model]

    if model_pricing is None:
        return 0.0

    input_cost = model_pricing["input"] * prompt_tokens
    output_cost = model_pricing["output"] * completion_tokens

    return round(input_cost + output_cost, 6)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

@app.get('/')
def root():
    return {
        "message" : "CostLens is running"
    }

@app.get('/health')
def health_check():
    return {
        "status": "ok"
    }

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest, db: Session=Depends(get_db), x_costlens_feature: str | None = Header(default = "unknown")):
    start_time = time.time()

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:

            response = await client.post(
                "https://api.openai.com/v1/chat/completions",

                headers = {
                    "Authorization": f"Bearer {OPENAI_API_KEY}"
                },

                json = request.model_dump()
            ) 
        end_time = time.time()
        latency_ms = round((end_time - start_time)*1000)

        openai_response = response.json()

        usage = openai_response.get("usage",{})

        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        total_tokens = usage.get("total_tokens", 0)

        estimated_cost = calculate_cost(request.model, prompt_tokens, completion_tokens)

        event = LLMEvent(

            feature = x_costlens_feature,

            model = request.model,

            prompt_tokens = prompt_tokens,

            completion_tokens = completion_tokens,

            total_tokens = total_tokens,

            estimated_cost = estimated_cost,

            latency_ms = latency_ms
        )

        db.add(event)
        db.commit()
        db.refresh(event)


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

    except httpx.ReadTimeout:
        raise HTTPException(
            status_code=504,
            detail="OpenAI took too long to respond. Try again."
        )

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.text
        )