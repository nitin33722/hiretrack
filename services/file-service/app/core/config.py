from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    STORAGE_BACKEND: Literal["local", "s3"] = "local"
    LOCAL_STORAGE_PATH: str = "./uploads"
    INTERNAL_SECRET:str
    MAX_FILE_SIZE_MB: int = 5
    ALLOWED_MIME_TYPES:str = "application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ENVIRONMENT: Literal["development", "production", "staging"] = "development"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    
    @property
    def max_file_size_bytes(self)->int:
        return self.MAX_FILE_SIZE_MB * 1024 *1024
    
    @property
    def allowed_mime_types_list(self)->list:
        return [mime.strip() for mime in self.ALLOWED_MIME_TYPES.split(",")]

settings = Settings()