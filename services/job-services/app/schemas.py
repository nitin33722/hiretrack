from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class JobCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=10)
    location: str = Field(min_length=1, max_length=255)
    salary_range: Optional[str] = None

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    is_active: Optional[bool] = None

class JobOut(BaseModel):
    id: int
    title: str
    description: str
    location: str
    salary_range: Optional[str]
    is_active: bool
    recruiter_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class JobListResponse(BaseModel):
    items: list[JobOut]
    total: int
    page: int
    limit: int
    pages: int

class JobExistsResponse(BaseModel):
    exists: bool
    job_id: Optional[int] = None