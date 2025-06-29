from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ORM: str = Field(
        default="sqlalchemy", json_schema_extra={"enum": ["sqlalchemy", "ponyorm"]}
    )
    DATABASE_PATH: str = Field(min_length=1)
    BLUELYTICS_API_URL: str = Field(min_length=1)

    model_config = {"env_file": "./app/.env"}


settings = Settings()

DATABASE_URL = f"sqlite:///{settings.DATABASE_PATH}"
BLUELYTICS_API_URL = settings.BLUELYTICS_API_URL
