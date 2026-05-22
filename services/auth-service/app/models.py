from sqlalchemy import Column, Integer, String, DateTime, func
from datetime import datetime, timezone
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime,  default = lambda : datetime.now(timezone.utc), nullable = False)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"