from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    AUTH_SERVICE_URL: str = "http://localhost:8001"
    JOB_SERVICE_URL: str = "http://localhost:8002"
    APPLICATION_SERVICE_URL: str = "http://localhost:8003"
    FILE_SERVICE_URL: str = "http://localhost:8004"
    ALLOWED_ORIGINS: list[str]
    # Environment
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    
    RATE_LIMIT: str = "100/minute"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()