from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from app.core.auth import auth_client

security = HTTPBearer(auto_error=False)

async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    result = await auth_client.verify_token(token)
    
    if not result.get("valid"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return {
        "user_id": result.get("user_id"),
        "role": result.get("role"),
        "email": result.get("email")
    }

async def require_recruiter(user: dict = Depends(get_current_user)) -> dict:
    """
    Dependency for recruiter-only endpoints.
    Requires authentication AND role must be "recruiter".
    """
    if user.get("role") != "recruiter":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters can access this endpoint"
        )
    return user

async def optional_user(credentials: HTTPBasicCredentials = Depends(security)) -> dict:
    if not credentials:
        return None
    
    token = credentials.credentials
    result = await auth_client.verify_token(token)
    
    if not result.get("valid"):
        return None
    
    return {
        "user_id": result.get("user_id"),
        "role": result.get("role"),
        "email": result.get("email")
    }