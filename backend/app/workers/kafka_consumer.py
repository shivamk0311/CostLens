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
                "bootstrap.servers": "kafka:9092",
                "group.id": "costlens-consumer",
                "auto.offset.reset": "earliest",
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

        create_llm_event(db=db, event=llm_event)

if __name__ == "__main__":
    start_consumer()