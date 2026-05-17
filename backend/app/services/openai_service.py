import os, httpx 
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


async def call_openai_chat_completion(payload : dict):

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:

            response = await client.post(
                "https://api.openai.com/v1/chat/completions",

                headers = {
                    "Authorization": f"Bearer {OPENAI_API_KEY}"
                },

                json = payload
            ) 

            return response.json()

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