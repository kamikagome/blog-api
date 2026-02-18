"""Application configuration"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    database_url: str = "sqlite:///./blog.db"
    app_name: str = "Blog API"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
