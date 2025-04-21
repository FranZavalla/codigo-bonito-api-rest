from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    ENV: str = Field(default="development", enumerate=["development", "production"])
    ORM: str = Field(default="sqlalchemy", enumerate=["sqlalchemy", "ponyorm"])

    class Config:
        env_file = ".env"


settings = Settings()

DATABASE_FILENAME = f"database_{settings.ENV}.sqlite"
DATABASE_URL = f"sqlite:///{DATABASE_FILENAME}"
