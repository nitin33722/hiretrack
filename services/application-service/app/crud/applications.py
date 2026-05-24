from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models import Application
from app.schemas import ApplicationCreate

class ApplicationService:

    @staticmethod
    def create_application(
        db: Session,
        data: ApplicationCreate,
        candidate_id: int,
        file_id: str = None,
        resume_filename: str = None,
        resume_url: str = None
    ) -> Application:
        application = Application(
            job_id=data.job_id,
            candidate_id=candidate_id,
            cover_letter=data.cover_letter,
            file_id=file_id,
            resume_filename=resume_filename,
            resume_url=resume_url,
            status="pending"
        )
        db.add(application)
        db.commit()
        db.refresh(application)
        return application
    
    @staticmethod
    def get_application(db: Session, application_id: int) -> Application:
        """Get a single application by ID"""
        return db.query(Application).filter(
            Application.id == application_id
        ).first()
    
    @staticmethod
    def get_candidate_applications(
        db: Session,
        candidate_id: int
    ) -> list[Application]:
        return db.query(Application).filter(
            Application.candidate_id == candidate_id
        ).order_by(desc(Application.applied_at)).all()
    
    @staticmethod
    def get_job_applications(
        db: Session,
        job_id: int
    ) -> list[Application]:
        return db.query(Application).filter(
            Application.job_id == job_id
        ).order_by(desc(Application.applied_at)).all()
    
    @staticmethod
    def update_status(
        db: Session,
        application_id: int,
        new_status: str
    ) -> Application:
        application = db.query(Application).filter(
            Application.id == application_id
        ).first()
        
        if not application:
            return None
        
        application.status = new_status
        db.commit()
        db.refresh(application)
        return application
    
    @staticmethod
    def already_applied(
        db: Session,
        job_id: int,
        candidate_id: int
    ) -> bool:
        return db.query(Application).filter(
            Application.job_id == job_id,
            Application.candidate_id == candidate_id
        ).first() is not None