from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes
    
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    
    
    DATABASE_URL: str = "sqlite:///./test.db"
    
    
    model_config = SettingsConfigDict(env_file="app/core/.env", env_file_encoding="utf-8",extra="ignore")
    

settings = Settings()
    
    