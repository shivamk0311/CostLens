import json 
import os
from confluent_kafka import Producer

# KAFKA_BOOTSTRAP_SERVERS = os.getenv(
#     "KAFKA_BOOTSTRAP_SERVERS",
#     "kafka:9092"
# )

producer = Producer({
    "bootstrap.servers": os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS",
        "kafka:9092"
    ),
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