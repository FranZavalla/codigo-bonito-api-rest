from pony.orm import db_session
from .models_ponyorm import db
from settings import settings


def init_pony():
    db.bind(provider="sqlite", filename=settings.DATABASE_PATH, create_db=True)
    db.generate_mapping(create_tables=True)
