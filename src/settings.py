from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    ORM: str = Field(default="sqlalchemy", enumerate=["sqlalchemy", "ponyorm"])
    DATABASE_PATH: str = Field(min_length=1)

    class Config:
        env_file = ".env"


settings = Settings()

DATABASE_URL = f"sqlite:///{settings.DATABASE_PATH}"
