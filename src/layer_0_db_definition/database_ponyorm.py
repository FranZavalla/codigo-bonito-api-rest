from pony.orm import db_session
from .models_ponyorm import db
from settings import DATABASE_FILENAME


sqlite_path = DATABASE_FILENAME

def init_pony():
    db.bind(provider="sqlite", filename=sqlite_path, create_db=True)
    db.generate_mapping(create_tables=True)

