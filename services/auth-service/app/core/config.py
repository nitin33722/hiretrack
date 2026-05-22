from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):

    DATABASE_URL:str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    INTERNAL_SECRET : str

    ENVIRONMENT : Literal["development","staging","production"] = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()