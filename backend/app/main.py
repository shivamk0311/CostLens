from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
import httpx
import os, time

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


app = FastAPI(
    title="CostLens API",
    version="0.1.0"
)

class Message(BaseModel):
    role: str 
    content: str 

class ChatCompletionRequest(BaseModel):
    model: str 
    messages: List[Message]
    temperature: Optional[float] = 0.7


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
async def chat_completions(request: ChatCompletionRequest):
    start_time = time.time()
    async with httpx.AsyncClient() as client:

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

    return {
        "costlens":{
            "latency_ms":latency_ms,
            "model": request.model
        },
        "openai_response": openai_response
    }