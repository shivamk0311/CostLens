from app.models.llm_event import LLMEvent
from sqlalchemy import func

def create_llm_event(
        db,
        feature,
        model,
        prompt_tokens,
        completion_tokens,
        total_tokens,
        estimated_cost,
        latency_ms
):
    event = LLMEvent(

            feature = feature,

            model = model,

            prompt_tokens = prompt_tokens,

            completion_tokens = completion_tokens,

            total_tokens = total_tokens,

            estimated_cost = estimated_cost,

            latency_ms = latency_ms
        )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


def get_recent_events(db, limit=20):
    events = (
        db.query(LLMEvent)
        .order_by(LLMEvent.created_at.desc())
        .limit(limit)
        .all()
    )

    return events

def get_cost_summary(db):
    summary = (
        db.query(
            func.count(LLMEvent.id).label("total_requests"),
            func.sum(LLMEvent.total_tokens).label("total_tokens"),
            func.sum(LLMEvent.estimated_cost).label("total_cost_usd"),
            func.avg(LLMEvent.latency_ms).label("average_latency_ms"),
        )
        .first()
    )

    return {
        "total_requests": summary.total_requests or 0,
        "total_tokens": summary.total_tokens or 0,
        "total_cost_usd": round(summary.total_cost_usd or 0, 6),
        "average_latency_ms": round(summary.average_latency_ms or 0, 2),
    }

def get_cost_by_feature(db):
    results = (
        db.query(
            LLMEvent.feature,
            func.sum(LLMEvent.estimated_cost).label("total_cost_usd")
        ).group_by(LLMEvent.feature).all()
    )

    return [
        {
            "feature" : row.feature,
            "total_cost_usd" : round(row.total_cost_usd or 0, 6)
        } for row in results
    ]

def get_cost_by_model(db):
    results = (
        db.query(
            LLMEvent.model,
            func.sum(LLMEvent.estimated_cost).label("total_cost_usd")
        ).group_by(LLMEvent.model).all()
    )

    return[
        {
            "model" : row.model,
            "total_cost_usd": round(row.total_cost_usd or 0, 6)
        } for row in results
    ]