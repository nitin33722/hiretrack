from fastapi import HTTPException, status
from abc import ABC, abstractmethod
from pathlib import Path
import uuid
from app.core.config import settings

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

def get_storage_backend() -> StorageBackend:
    if settings.STORAGE_BACKEND == "local":
        return LocalStorageBackend()
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail = "storage backend not defined"
    )