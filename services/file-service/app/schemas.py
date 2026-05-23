from pydantic import BaseModel
from typing import Optional

class FileUploadResponse(BaseModel):
    file_id:str
    file_name:str
    url:str
    size_bytes:int

class FileDeleteResponse(BaseModel):
    success:bool
    file_id:str
    