from sqlalchemy import create_engine
from .models_sqlalchemy import Base
from settings import DATABASE_URL
from sqlalchemy.orm import sessionmaker


engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_database():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
