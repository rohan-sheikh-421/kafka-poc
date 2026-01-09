import os
import json
from confluent_kafka import Producer

producer = None

def get_producer():
    global producer
    if producer is None:
        producer = Producer({
            "bootstrap.servers": os.environ["KAFKA_BOOTSTRAP_SERVERS"]
        })
    return producer

def publish_order(order):
    event = {
        "orderId": order.id,
        "item": order.item,
        "quantity": order.quantity
    }

    p = get_producer()
    p.produce("order-events", json.dumps(event).encode("utf-8"))
    p.flush()
