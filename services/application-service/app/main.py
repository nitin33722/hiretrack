from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db, engine, Base
from app.core.config import settings
from app.core.clients import job_client, file_client
from app.schemas import (
    ApplicationOut,
    ApplicationWithJob,
    ApplicationWithCandidate,
    ApplicationStatusUpdate
)
from app.crud.applications import ApplicationService
from app.dependencies.auth import get_current_user, require_candidate, require_recruiter
from app.models import Application

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Application Service",
    description="Job application management",
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
    return {
        "status": "healthy",
        "service": "application-service",
        "version": "1.0.0"
    }

@app.post("/applications", response_model=ApplicationOut, status_code=201)
async def submit_application(
    job_id: int = Form(...),
    cover_letter: Optional[str] = Form(None),
    resume: Optional[UploadFile] = File(None),
    user: dict = Depends(require_candidate),
    db: Session = Depends(get_db)
):
    candidate_id = user.get("user_id")
    
    job_exists = await job_client.job_exists(job_id)
    if not job_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found or no longer active"
        )
    
    already_applied = ApplicationService.already_applied(db, job_id, candidate_id)
    if already_applied:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already applied to this job"
        )
    
    file_id = None
    resume_filename = None
    resume_url = None
    
    if resume:
        file_bytes = await resume.read()
        file_result = await file_client.upload_resume(file_bytes, resume.filename)
        file_id = file_result.get("file_id")
        resume_filename = file_result.get("filename")
        resume_url = file_result.get("url")
    
    from app.schemas import ApplicationCreate
    application_data = ApplicationCreate(
        job_id=job_id,
        cover_letter=cover_letter
    )
    
    application = ApplicationService.create_application(
        db=db,
        data=application_data,
        candidate_id=candidate_id,
        file_id=file_id,
        resume_filename=resume_filename,
        resume_url=resume_url
    )
    
    return application

@app.get("/applications/me", response_model=list[ApplicationWithJob])
async def get_my_applications(
    user: dict = Depends(require_candidate),
    db: Session = Depends(get_db)
):

    candidate_id = user.get("user_id")
    
    applications = ApplicationService.get_candidate_applications(db, candidate_id)
    
    if not applications:
        return []
    
    job_ids = list(set(app.job_id for app in applications))
    
    jobs_map = await job_client.get_jobs_batch(job_ids)
    
    enriched = []
    for app in applications:
        job_data = jobs_map.get(app.job_id, {})
        enriched.append(ApplicationWithJob(
            **app.__dict__,
            job_title=job_data.get("title"),
            job_location=job_data.get("location"),
            job_salary_range=job_data.get("salary_range")
        ))
    
    return enriched

@app.get("/applications/job/{job_id}", response_model=list[ApplicationOut])
async def get_job_applications(
    job_id: int,
    user: dict = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    recruiter_id = user.get("user_id")
    
    job_recruiter_id = await job_client.get_recruiter_id(job_id)
    
    if job_recruiter_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    if job_recruiter_id != recruiter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't own this job"
        )
    
    applications = ApplicationService.get_job_applications(db, job_id)
    return applications

@app.patch("/applications/{application_id}/status", response_model=ApplicationOut)
async def update_application_status(
    application_id: int,
    status_update: ApplicationStatusUpdate,
    user: dict = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    recruiter_id = user.get("user_id")
    
    application = ApplicationService.get_application(db, application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    job_recruiter_id = await job_client.get_recruiter_id(application.job_id)
    
    if job_recruiter_id != recruiter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't own the job for this application"
        )
    
    updated = ApplicationService.update_status(
        db, application_id, status_update.status
    )
    
    return updated