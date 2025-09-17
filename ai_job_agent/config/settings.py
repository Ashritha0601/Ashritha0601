import os
from typing import List, Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application settings
    app_name: str = "AI Job Agent"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # OpenAI settings
    openai_api_key: Optional[str] = None
    
    # Email settings
    email_host: str = "smtp.gmail.com"
    email_port: int = 587
    email_username: Optional[str] = None
    email_password: Optional[str] = None
    
    # User settings
    user_email: str = "work.ashrithabattula@gmail.com"
    user_name: str = "Ashritha Battula"
    
    # Job search settings
    default_location: str = "Dallas, TX"
    max_jobs_per_search: int = 50
    job_alert_frequency_hours: int = 24
    
    # Resume settings
    resume_storage_path: str = "data/resumes"
    cover_letter_storage_path: str = "data/cover_letters"
    
    # External API settings (optional)
    linkedin_api_key: Optional[str] = None
    indeed_api_key: Optional[str] = None
    glassdoor_api_key: Optional[str] = None
    
    # AI model settings
    default_ai_model: str = "gpt-3.5-turbo"
    ai_temperature: float = 0.3
    max_tokens: int = 2000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create global settings instance
settings = Settings()