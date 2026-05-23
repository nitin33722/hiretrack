from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    DATBASE_URL: str
    AUTH_SERVICE_URL: str = "https://localhost:8001"
    INTERNAL_SECRET: str
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    
    class Config:
        env_file = ".evn"
        case_sensitive = True

settings = Settings()