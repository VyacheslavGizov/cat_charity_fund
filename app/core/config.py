from pydantic import BaseSettings


MAX_NAME_LENGTH = 100
MIN_NAME_LENGTH = 1
MIN_DESCRIPTION_LENGTH = 1


class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = '.env'


settings = Settings()
