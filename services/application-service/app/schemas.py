from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from datetime import datetime

ApplicationStatus = Literal["pending", "reviewed", "accepted", "rejected"]

class ApplicationCreate(BaseModel):
    job_id: int
    cover_letter: Optional[str] = None

class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus

class ApplicationOut(BaseModel):
    id: int
    job_id: int
    candidate_id: int
    file_id: Optional[str]
    resume_filename: Optional[str]
    resume_url: Optional[str]
    cover_letter: Optional[str]
    status: str
    applied_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ApplicationWithJob(ApplicationOut):
    job_title: Optional[str] = None
    job_location: Optional[str] = None
    job_salary_range: Optional[str] = None

class ApplicationWithCandidate(ApplicationOut):
    candidate_email: Optional[str] = None
    candidate_name: Optional[str] = None