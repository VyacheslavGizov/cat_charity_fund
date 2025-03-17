from pydantic import BaseSettings, EmailStr
from typing import Optional


MAX_NAME_LENGTH = 100
MIN_NAME_LENGTH = 1
MIN_DESCRIPTION_LENGTH = 1


class Settings(BaseSettings):
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
