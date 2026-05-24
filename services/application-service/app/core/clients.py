import httpx
from fastapi import HTTPException,status
from app.core.config import settings

class AuthServiceClient:
    def __init__(self):
        self.base_url = settings.AUTH_SERVICE_URL
        self.timeout = 3.0

    async def verify_token(self, token:str) -> dict:
        payload = {
            "token": token,
            "internal_secret":settings.INTERNAL_SECRET
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/auth/verify-token",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Auth service unavailable"
            )
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Auth Service error: {str(e)}"
            )

class JobServiceClient:
    def __init__(self):
        self.base_url = settings.JOB_SERVICE_URL
        self.timeout = 3.0

    async def job_exists(self, job_id: int) ->bool:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/jobs/{job_id}/exists"
                )
                response.raise_for_status()
                data = response.json()
                return data.get("exists", False)
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Job Service unavailable"
            )
        except httpx.HTTPError:
            return False
    
    async def get_job(self, job_id:int)->dict:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/jobs/{job_id}"
                )
                response.raise_for_status()
                return response.json()
        except Exception:
            return None
    async def get_jobs_batch(self, job_ids:list[int])->dict:
        if not job_ids:
            return {}
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/jobs/batch",
                    json=job_ids
                )
                response.raise_for_status()
                data = response.json()
                return {job["id"]: job for job in data.get("jobs", [])}
        except Exception:
            return {}
    async def get_recruiter_id(self, job_id: int) -> int:
        job = await self.get_job(job_id)
        if not job:
            return None
        return job.get("recruiter_id")

class FileServiceClient:
    def __init__(self):
        self.base_url = settings.FILE_SERVICE_URL
        self.timeout = 10.0
    
    async def upload_resume(self, file_bytes: bytes, filename: str) -> dict:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/files/upload",
                    headers={"internal-secret": settings.INTERNAL_SECRET},
                    files={"file": (filename, file_bytes, "application/pdf")}
                )
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="File service unavailable"
            )
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"File upload failed: {str(e)}"
            )
    
    async def delete_resume(self, file_id: str) -> bool:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.delete(
                    f"{self.base_url}/files/{file_id}",
                    headers={"internal-secret": settings.INTERNAL_SECRET}
                )
                response.raise_for_status()
                return True
        except Exception:
            return False
    
auth_client = AuthServiceClient()
job_client = JobServiceClient()
file_client = FileServiceClient()