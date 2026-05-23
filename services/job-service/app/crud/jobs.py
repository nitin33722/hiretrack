from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models import Job
from app.schemas import JobCreate, JobUpdate

class JobService:
    @staticmethod
    def create_job(db: Session, data: JobCreate, recruiter_id: int) -> Job:
        job = Job(
            title=data.title,
            description=data.description,
            location=data.location,
            salary_range=data.salary_range,
            recruiter_id=recruiter_id
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return job
    
    @staticmethod
    def get_job(db: Session, job_id: int) -> Job:
        return db.query(Job).filter(Job.id == job_id).first()
    
    @staticmethod
    def get_jobs(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        title_filter: str = None,
        location_filter: str = None,
        is_active_only: bool = True
    ) -> tuple[list[Job], int]:
        query = db.query(Job)
        
        if is_active_only:
            query = query.filter(Job.is_active == True)
        
        if title_filter:
            query = query.filter(Job.title.ilike(f"%{title_filter}%"))
        
        if location_filter:
            query = query.filter(Job.location.ilike(f"%{location_filter}%"))
        
        total = query.count()
        
        query = query.order_by(desc(Job.created_at))
        
        jobs = query.offset(skip).limit(limit).all()
        
        return jobs, total
    
    @staticmethod
    def get_recruiter_jobs(db: Session, recruiter_id: int) -> list[Job]:
        return db.query(Job).filter(Job.recruiter_id == recruiter_id).all()
    
    @staticmethod
    def update_job(db: Session, job_id: int, data: JobUpdate, recruiter_id: int) -> Job:

        job = db.query(Job).filter(Job.id == job_id).first()
        
        if not job:
            return None
        
        if job.recruiter_id != recruiter_id:
            raise PermissionError("You don't own this job")
        
        if data.title is not None:
            job.title = data.title
        if data.description is not None:
            job.description = data.description
        if data.location is not None:
            job.location = data.location
        if data.salary_range is not None:
            job.salary_range = data.salary_range
        if data.is_active is not None:
            job.is_active = data.is_active
        
        db.commit()
        db.refresh(job)
        return job
    
    @staticmethod
    def delete_job(db: Session, job_id: int, recruiter_id: int) -> bool:
        job = db.query(Job).filter(Job.id == job_id).first()
        
        if not job:
            return False
        
        if job.recruiter_id != recruiter_id:
            raise PermissionError("You don't own this job")
        
        job.is_active = False
        db.commit()
        return True
    
    @staticmethod
    def job_exists(db: Session, job_id: int) -> bool:
        return db.query(Job).filter(
            Job.id == job_id,
            Job.is_active == True
        ).first() is not None