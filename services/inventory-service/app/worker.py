import json
from . import db
from .models import Inventory
from .kafka_client import create_consumer, create_producer, publish_inventory_event

def main():
    db.init_db()
    db.Base.metadata.create_all(bind=db.engine)

    consumer = create_consumer()
    producer = create_producer()

    consumer.subscribe(["order-events"])
    print("📦 Inventory Service listening to order-events")

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Kafka error:", msg.error())
            continue

        event = json.loads(msg.value().decode())
        print("➡️ Received:", event)

        session = db.get_session()

        inv = Inventory(
            order_id=event["orderId"],
            item=event["item"],
            quantity=event["quantity"],   
            status="RESERVED"
        )

        session.add(inv)
        session.commit()
        session.close()

        publish_inventory_event(producer, {
            "orderId": event["orderId"],
            "status": "RESERVED"
        })

if __name__ == "__main__":
    main()
