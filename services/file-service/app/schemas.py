from pydantic import BaseModel
from typing import Optional

class FileUploadResponse(BaseModel):
    file_id:str
    filename:str
    url:str
    size_bytes:int

class FileDeleteResponse(BaseModel):
    success:bool
    file_id:str
    