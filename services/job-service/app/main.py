from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.database import get_db, engine, Base
from app.core.config import settings
from app.schemas import (
    JobCreate, JobUpdate, JobOut, JobExistsResponse, JobListResponse
)
from app.crud.jobs import JobService
from app.dependencies.auth import get_current_user, require_recruiter, optional_user
from app.models import Job
Base.metadata.create_all(bind=engine)

app=FastAPI(
    title="JobService",
    description="Job posting Management",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "job-service",
        "version": "1.0.0"
    }

@app.get("/jobs", response_model = JobListResponse)
async def list_jobs(
    title: str = Query(None),
    location: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user: dict = Depends(optional_user),
    db: Session = Depends(get_db)
):  
    skip = (page-1)*limit
    if user and user.get("role") == "recruiter":
        jobs = JobService.get_recruiter_jobs(db, user.get("user_id"))
        total = len(jobs)
        items = jobs[skip:skip+limit]
    else:
        items, total = JobService.get_jobs(
            db,
            skip=skip,
            limit=limit,
            title_filter=title,
            location_filter=location,
            is_active_only=True
        )
    
    pages = (total + limit - 1) // limit
    
    return JobListResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=pages
    )
@app.get("/jobs/{job_id}", response_model=JobOut)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    job = JobService.get_job(db, job_id)
    
    if not job or not job.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return job

@app.post("/jobs", response_model=JobOut, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_data: JobCreate,
    user: dict = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    job = JobService.create_job(db, job_data, user.get("user_id"))
    return job

@app.put("/jobs/{job_id}", response_model=JobOut)
async def update_job(
    job_id: int,
    job_data: JobUpdate,
    user: dict = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    try:
        job = JobService.update_job(db, job_id, job_data, user.get("user_id"))
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't own this job"
        )
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return job

@app.delete("/jobs/{job_id}")
async def delete_job(
    job_id: int,
    user: dict = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    try:
        success = JobService.delete_job(db, job_id, user.get("user_id"))
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't own this job"
        )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return {"message": "Job deleted successfully"}

@app.get("/jobs/{job_id}/exists", response_model=JobExistsResponse)
async def job_exists(job_id: int, db: Session = Depends(get_db)):
    exists = JobService.job_exists(db, job_id)
    return JobExistsResponse(
        exists=exists,
        job_id=job_id if exists else None
    )

@app.post("/jobs/batch")
async def get_jobs_batch(
    job_ids: list[int],
    db: Session = Depends(get_db)
):
    jobs = db.query(Job).filter(Job.id.in_(job_ids)).all()
    return {"jobs": jobs}