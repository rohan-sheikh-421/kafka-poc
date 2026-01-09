from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import db
from .models import Order
from .kafka_client import publish_order

app = FastAPI(title="Order Service")

@app.on_event("startup")
def startup():
    db.init_db()
    db.Base.metadata.create_all(bind=db.engine)

class OrderCreate(BaseModel):
    item: str
    quantity: int

def get_db():
    session = db.get_session()
    try:
        yield session
    finally:
        session.close()

@app.post("/orders")
def create_order(req: OrderCreate, db_session: Session = Depends(get_db)):
    order = Order(item=req.item, quantity=req.quantity)
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    publish_order(order)

    return {
        "id": order.id,
        "item": order.item,
        "quantity": order.quantity
    }
