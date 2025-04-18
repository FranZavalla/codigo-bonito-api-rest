from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    ENV: str = Field(default="development", enumerate=["development", "production"])

    class Config:
        env_file = ".env"


settings = Settings()

DATABASE_FILENAME = f"database_{settings.ENV}.sqlite"
