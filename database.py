from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Calllog(Base):
    __tablename__ = "call_logs"
    id = Column(Integer, primary_key=True, index=True)
    model_used = Column(String, index=True)
    complexity = Column(String, index=True)
    tokens_used = Column(Integer)
    cost_usd = Column(Float)
    latency_seconds = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)