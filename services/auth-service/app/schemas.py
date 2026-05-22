from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8),
    full_name: str = Field(min_length=1, max_length=100)
    role: Literal["recruiter", "candidate"]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserOut"

class UserOut(BaseModel):
    id:int
    email:EmailStr
    full_name: str
    role: str
    create_at: str

class TokenPayload(BaseModel):
    sub: str
    role: str
    email: str

class VerifyTokenResponse(BaseModel):
    valid: bool
    user_id: int = None
    role: str = None
    email: str = None
