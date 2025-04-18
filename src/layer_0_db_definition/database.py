from sqlalchemy import create_engine
from .models import Base
from settings import DATABASE_FILENAME
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"sqlite:///{DATABASE_FILENAME}"

engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_database():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
