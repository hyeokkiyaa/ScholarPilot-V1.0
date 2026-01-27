import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./data/scholarpilot.db"
    DATA_DIR: str = "./data"
    
    # Optional: External API Keys (can also be set in DB settings table)
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    
    class Config:
        env_file = ".env"

settings = Settings()
