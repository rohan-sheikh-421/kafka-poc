import os, time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.environ["DATABASE_URL"]

engine = None
SessionLocal = None

class Base(DeclarativeBase):
    pass

def init_db(retries=10, delay=2):
    global engine, SessionLocal
    for i in range(retries):
        try:
            engine = create_engine(DATABASE_URL, pool_pre_ping=True)
            SessionLocal = sessionmaker(bind=engine)
            engine.connect().close()
            print("✅ Notification DB connected")
            return
        except OperationalError:
            print(f"⏳ Notification DB retry {i+1}/{retries}")
            time.sleep(delay)
    raise RuntimeError("❌ Notification DB failed")

def get_session():
    if SessionLocal is None:
        raise RuntimeError("❌ Notification DB not initialized")
    return SessionLocal()
