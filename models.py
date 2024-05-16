from sqlalchemy import JSON, Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
import datetime

Base = declarative_base()

class SpiderStatus(enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class SpiderTask(Base):
    __tablename__ = 'spider_tasks'
    
    id = Column(Integer, primary_key=True, index=True)
    spider_name = Column(String(50), nullable=False)
    start_url = Column(Text, nullable=False)
    parameters = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    status = Column(Enum(SpiderStatus), default=SpiderStatus.PENDING)
    logs = relationship("SpiderLog", back_populates="task")

class SpiderLog(Base):
    __tablename__ = 'spider_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('spider_tasks.id'), nullable=False)
    log_message = Column(Text, nullable=False)
    total_urls_scraped = Column(Integer, nullable=True)
    successful_requests = Column(Integer, nullable=True)
    failed_requests = Column(Integer, nullable=True)
    status_codes = Column(JSON, nullable=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=True)  # Duration in seconds
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    task = relationship("SpiderTask", back_populates="logs")
