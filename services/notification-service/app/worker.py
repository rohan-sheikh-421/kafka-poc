import os
import json
from confluent_kafka import Consumer
from . import db
from .models import Notification

def main():
    db.init_db()
    db.Base.metadata.create_all(bind=db.engine)

    consumer = Consumer({
        "bootstrap.servers": os.environ["KAFKA_BOOTSTRAP_SERVERS"],
        "group.id": "notification-service",
        "auto.offset.reset": "earliest"
    })

    consumer.subscribe(["inventory-events"])
    print("🔔 Notification Service listening to inventory-events")

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Kafka error:", msg.error())
            continue

        event = json.loads(msg.value().decode())
        message = f"Order {event['orderId']} is {event['status']}"

        print("📨 Sending notification:", message)

        session = db.get_session()
        session.add(Notification(order_id=event["orderId"], message=message))
        session.commit()
        session.close()

if __name__ == "__main__":
    main()
