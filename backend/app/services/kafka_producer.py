import json 
import os
from confluent_kafka import Producer

KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "kafka:9092"
)

producer = Producer({
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS
})

def delivery_report(err,msg):
    if err:
        print(f"Kafka  delivery failed: {err}.")
    else:
        print(f"Kafka message delivered to {msg.topic()} [{msg.partition()}]")

def publish_llm_event(event: dict):
    producer.produce(
        "costlens.events.raw",
        key= str(event.get("id", "")),
        value= json.dumps(event),
        callback= delivery_report
    )

    producer.flush()