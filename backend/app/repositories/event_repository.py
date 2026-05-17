from app.models.llm_event import LLMEvent

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