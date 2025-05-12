from app.settings import settings

from app.layer_0_db_definition.models_ponyorm import db


def init_pony():
    db.bind(provider="sqlite", filename=settings.DATABASE_PATH, create_db=True)
    db.generate_mapping(create_tables=True)
