from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from app.core.clients import auth_client

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security)
) -> dict:
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

async def require_candidate(
    user: dict = Depends(get_current_user)
) -> dict:
    if user.get("role") != "candidate":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only candidates can access this endpoint"
        )
    return user

async def require_recruiter(
    user: dict = Depends(get_current_user)
) -> dict:
    if user.get("role") != "recruiter":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters can access this endpoint"
        )
    return user