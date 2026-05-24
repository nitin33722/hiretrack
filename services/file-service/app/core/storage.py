from fastapi import HTTPException, status
from abc import ABC, abstractmethod
from pathlib import Path
import uuid
from app.core.config import settings
import boto3

class StorageBackend(ABC):
    @abstractmethod
    async def save(self, file_bytes:bytes, original_filename:str, file_id:str = None) -> dict:
        pass
    @abstractmethod
    async def get(self, file_id:str) -> bytes:
        pass
    @abstractmethod
    async def delete(self, file_id:str) -> bool:
        pass

class LocalStorageBackend(StorageBackend):
    def __init__(self):
        self.storage_path = Path(settings.LOCAL_STORAGE_PATH)
        self.storage_path.mkdir(parents = True, exist_ok=True)

    async def save(self, file_bytes:bytes, original_filename: str, file_id:str = None) -> dict:
        if file_id is None:
            file_id = str(uuid.uuid4())
        extension = Path(original_filename).suffix
        unique_filename = f"{file_id}{extension}"
        file_path = self.storage_path / unique_filename
        file_path.write_bytes(file_bytes)
        
        return {
            "file_id": file_id,
            "filename": original_filename,
            "path": str(file_path),
            "url": f"/files/{file_id}/download"
        }
    
    async def get(self, file_id: str) -> bytes:
        matching_files = list(self.storage_path.glob(f"{file_id}*"))
        
        if not matching_files:
            raise FileNotFoundError(f"File {file_id} not found")
        
        file_path = matching_files[0]
        return file_path.read_bytes()
    
    async def delete(self, file_id):
        matching_files = list(self.storage_path.glob(f"{file_id}*"))
        
        if not matching_files:
            return False
        
        matching_files[0].unlink() 
        return True
class S3StorageBackend(StorageBackend):
    def __init__(self, bucket, region, access_key, secret_key):
        self.bucket = bucket
        self.s3_client = boto3.client(
            's3',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
    
    def upload(self, file_id: str, file_content: bytes, mime_type: str) -> str:
        self.s3_client.put_object(
            Bucket=self.bucket,
            Key=file_id,
            Body=file_content,
            ContentType=mime_type
        )
        return f"s3://{self.bucket}/{file_id}"
    
    def download(self, file_id: str) -> bytes:
        response = self.s3_client.get_object(Bucket=self.bucket, Key=file_id)
        return response['Body'].read()
    
    def delete(self, file_id: str) -> bool:
        self.s3_client.delete_object(Bucket=self.bucket, Key=file_id)
        return True
def get_storage_backend() -> StorageBackend:
    if settings.STORAGE_BACKEND == "local":
        return LocalStorageBackend(settings.LOCAL_STORAGE_PATH)
    elif settings.STORAGE_BACKEND == "s3":
        return S3StorageBackend(
            bucket=settings.AWS_S3_BUCKET,
            region=settings.AWS_S3_REGION,
            access_key=settings.AWS_ACCESS_KEY_ID,
            secret_key=settings.AWS_SECRET_ACCESS_KEY
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Unknown storage backend: {settings.STORAGE_BACKEND}"
    )
