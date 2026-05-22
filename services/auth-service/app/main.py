from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.database import get_db, engine, Base
from app.core.config import settings
from app.core.sercurity import (hash_password, verify_password, create_access_token, decode_token)
from app.models import User
from app.schemas import (
    UserLogin,
    UserRegister,
    UserOut,
    TokenResponse,
    VerifyTokenResponse
)
Base.metadata.crete_all(bind=engine)

app = FastAPI(
    title = "AuthService",
    description= "User authorization and token verification",
    vesrion= "1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "auth-service",
        "version": "1.0.0"
    }
@app.post("/auth/register", response_model=TokenResponse)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    hashed_pwd = hash_password(user_data.password)

    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pwd,
        full_name=user_data.full_name,
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_access_token(
        data={
            "sub": str(new_user.id),
            "role": new_user.role,
            "email": new_user.email
        }
    )

    return TokenResponse(
        access_token=token,
        user=UserOut.model_validate(new_user)
    )

@app.post("/auth/login", response_model = TokenResponse)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password"
        )
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    token = create_access_token(
        data={
            "sub":str(user.id),
            "role":user.role,
            "email":user.email
        }
    )
    return TokenResponse(
        access_token=token,
        user = UserOut.model_validate(user)
    )

def verify_internal_secret(internal_secret:str = None) -> bool:
    if internal_secret!=settings.INTERNAL_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detai = "Unauthorized"
        )
    return True

@app.post("/auth/verify-token")
async def verfify_token(
    token:str,
    internal_secret:str = None,
    db: Session = Depends(get_db)
):
    verify_internal_secret(internal_secret)
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
        role = payload.get("role")
        email = payload.get("email")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return VerifyTokenResponse(valid=False)
        
        return VerifyTokenResponse(
            valid=True,
            user_id=user_id,
            role=role,
            email=email
        )

    except Exception:
        return VerifyTokenResponse(valid = False)

@app.get("/auth/users/{user_id}")
async def get_user(
    user_id: int,
    internal_secret: str = None,
    db: Session = Depends(get_db)
):

    verify_internal_secret(internal_secret)
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserOut.model_validate(user)