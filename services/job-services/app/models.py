from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, func
from app.core.database import Base
from datetime import datetime

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    location = Column(String(255), nullable=False, index=True)
    salary_range = Column(String(100), nullable=True)  # e.g., "80000-120000"
    is_active = Column(Boolean, default=True, nullable=False)
    recruiter_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Job(id={self.id}, title={self.title}, recruiter_id={self.recruiter_id})>"