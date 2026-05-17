from fastapi import FastAPI

from app.database.connection import engine, Base
from app.routes import proxy, events, analytics
from app.models.llm_event import LLMEvent



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CostLens API",
    version="0.1.0"
)

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
