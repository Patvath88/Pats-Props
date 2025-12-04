import os
from sqlalchemy import create_engine, Column, String, JSON, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

DATABASE_URL = "sqlite:///api_cache.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class OddsApiCache(Base):
    __tablename__ = "odds_api_cache"
    game_id = Column(String, primary_key=True, index=True)
    odds_data = Column(JSON)
    fetched_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
