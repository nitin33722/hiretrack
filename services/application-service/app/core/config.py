from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
class Settings(BaseSettings):
    DATABASE_URL:str
    AUTH_SERVICE_URL: str = "http://localhost:8001"
    JOB_SERVICE_URL: str = "http://localhost:8002"
    FILE_SERVICE_URL: str = "http://localhost:8004"
    INTERNAL_SECRET: str
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()