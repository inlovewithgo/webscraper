from sqlalchemy import Column, Integer, String, JSON, DateTime
from app.database import Base
from datetime import datetime

class ScrapeTask(Base):
    __tablename__ = "scrape_tasks"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    status = Column(String, default="queued")
    pdf_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ScrapeResult(Base):
    __tablename__ = "scrape_results"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer)
    data = Column(JSON)
