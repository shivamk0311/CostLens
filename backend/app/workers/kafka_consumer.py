import os 
import json 
from confluent_kafka import Consumer
import time

from app.database.connection import SessionLocal
from app.repositories.event_repository import create_llm_event
from app.schemas.event import LLMEventCreate

KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "kafka:9092"
)

def create_consumer_with_retry():
    while True:
        try:
            consumer = Consumer({
                "bootstrap.servers": os.getenv(
                    "KAFKA_BOOTSTRAP_SERVERS",
                    "kafka:9092"
                ),
                "group.id": "costlens-consumer",
                "auto.offset.reset": "earliest",
                "security.protocol": os.getenv(
                    "KAFKA_SECURITY_PROTOCOL",
                    "PLAINTEXT"
                ),

                "sasl.mechanism": os.getenv(
                    "KAFKA_SASL_MECHANISM",
                    "PLAIN"
                ),

                "sasl.username": os.getenv(
                    "KAFKA_SASL_USERNAME",
                    ""
                ),

                "sasl.password": os.getenv(
                    "KAFKA_SASL_PASSWORD",
                    ""
                ),

                "session.timeout.ms": 60000,
                "heartbeat.interval.ms": 10000,
                "max.poll.interval.ms": 300000,

                "enable.auto.commit": False,
            })

            consumer.list_topics(timeout=5)
            print("Kafka consumer connected")
            return consumer

        except Exception as e:
            print(f"Kafka not ready yet: {e}")
            time.sleep(5)

consumer = create_consumer_with_retry()

consumer.subscribe(["costlens.events.raw"])

def start_consumer():
    print("Kafka consumer started...")

    db = SessionLocal()

    while True:
        msg =  consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        
        event = json.loads(
            msg.value().decode('utf-8')
        )

        print("Event received from Kafka.",event)
        llm_event = LLMEventCreate(**event)

        try:
            create_llm_event(
                db=db,
                feature=event.get("feature", "unknown"),
                model=event["model"],
                prompt_tokens=event.get("prompt_tokens", 0),
                completion_tokens=event.get("completion_tokens", 0),
                total_tokens=event.get("total_tokens", 0),
                estimated_cost=event.get("estimated_cost", 0),
                latency_ms=event.get("latency_ms", 0),
                cache_hit=event.get("cache_hit", False),
                cache_type=event.get("cache_type")
            )

            consumer.commit(
                message=msg,
                asynchronous=False
            )
        
        except Exception as e:
            db.rollback()
            print("Failed to persist Kafka event:", e)

        finally:
            db.close()
        

if __name__ == "__main__":
    start_consumer()