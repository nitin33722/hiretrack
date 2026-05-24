from sqlalchemy import Column, Integer, String, Text, DateTime
from app.core.database import Base
from datetime import datetime

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    
    job_id = Column(Integer, nullable=False, index=True)
    candidate_id = Column(Integer, nullable=False, index=True)
    
    file_id = Column(String, nullable=True)
    resume_filename = Column(String, nullable=True)
    resume_url = Column(String, nullable=True)
    
    cover_letter = Column(Text, nullable=True)
    
    status = Column(String, nullable=False, default="pending")
    
    applied_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Application(id={self.id}, job_id={self.job_id}, candidate_id={self.candidate_id}, status={self.status})>"