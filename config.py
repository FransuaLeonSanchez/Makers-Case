from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    app_name: str = "Makers Tech ChatBot"
    database_url: str = "sqlite+aiosqlite:///./makers_tech.db"
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY", "")
    use_mock_llm: bool = True
    cors_origins: list = ["*"]
    
    class Config:
        env_file = ".env"

settings = Settings() 