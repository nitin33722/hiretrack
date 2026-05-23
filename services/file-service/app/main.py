from fastapi import FastAPI, UploadFile, File, HTTPException, status, Header
from fastapi.responses import FileResponse
from app.core.config import settings
from app.core.storage import get_storage_backend
from app.schemas import FileDeleteResponse, FileUploadResponse

app = FastAPI(
    title = "File Service",
    description="File Upload and storage service",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "file-service",
        "version": "1.0.0"
    }

def verify_internal_secret(internal_secret:str=None)->bool:
    if internal_secret != settings.INTERNAL_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="unauthorized"
        )
    return True

def validate_file(file: UploadFile)->None:
    if file.content_type not in settings.allowed_mime_types_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = f"File type {file.content_type} not allowed. Allowed types: {settings.ALLOWED_MIME_TYPES}"
        )
    
@app.post("/files/upload", response_model=FileUploadResponse)
async def upload_file(
    file:UploadFile = File(...),
    internal_secret: str = Header(None)
):
    verify_internal_secret(internal_secret)
    validate_file(file)
    file_bytes = await file.read()
    if len(file_bytes) > settings.max_file_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds limit of {settings.MAX_FILE_SIZE_MB}MB"
        )
    storage = get_storage_backend()
    result = await storage.save(file_bytes, file.filename)
    
    return FileUploadResponse(
        file_id=result["file_id"],
        filename=result["filename"],
        url=result["url"],
        size_bytes=len(file_bytes)
    )
@app.get("/files/{file_id}/download")
async def download_file(file_id: str):
    try:
        storage = get_storage_backend()
        file_bytes = await storage.get(file_id)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Return file as download
    return FileResponse(
        content=file_bytes,
        filename=file_id,
        media_type="application/octet-stream"
    )

@app.delete("/files/{file_id}")
async def delete_file(
    file_id: str,
    internal_secret: str = Header(None)
):
    verify_internal_secret(internal_secret)
    
    try:
        storage = get_storage_backend()
        success = await storage.delete(file_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    return FileDeleteResponse(success=True, file_id=file_id)