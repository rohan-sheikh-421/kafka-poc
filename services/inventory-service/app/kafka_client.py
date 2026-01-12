import os, json
from confluent_kafka import Consumer, Producer

BOOTSTRAP = os.environ["KAFKA_BOOTSTRAP_SERVERS"]

def create_consumer():
    return Consumer({
        "bootstrap.servers": BOOTSTRAP,
        "group.id": "inventory-service",
        "auto.offset.reset": "earliest", 
        "enable.auto.commit": True
    })

def create_producer():
    return Producer({
        "bootstrap.servers": BOOTSTRAP
    })

def publish_inventory_event(producer, event):
    producer.produce("inventory-events", json.dumps(event).encode())
    producer.flush()
