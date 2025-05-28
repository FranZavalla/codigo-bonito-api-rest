from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.layer_0_db_definition.models_sqlalchemy import Base
from app.settings import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_sqlalchemy():
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_database():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
