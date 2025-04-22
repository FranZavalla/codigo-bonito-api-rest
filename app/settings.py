from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ORM: str = Field(default="sqlalchemy", enumerate=["sqlalchemy", "ponyorm"])
    DATABASE_PATH: str = Field(min_length=1)

    class Config:
        env_file = "./app/.env"


settings = Settings()

DATABASE_URL = f"sqlite:///{settings.DATABASE_PATH}"
