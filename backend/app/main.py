from fastapi import FastAPI

from app.database.connection import engine, Base
from app.routes import proxy, events, analytics
from app.models.llm_event import LLMEvent
from app.models.semantic_cache import SemanticCache
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="CostLens API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,

    allow_origins = [
        "http://localhost:3000"
    ],

    allow_credentials = True,

    allow_methods = ["*"],

    allow_headers = ["*"],
)

Base.metadata.create_all(bind=engine)

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

app.include_router(proxy.router)
app.include_router(events.router)
app.include_router(analytics.router)
