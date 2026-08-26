import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use a local SQLite db for initial development and testing to keep setup lightweight
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./poderbr.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=(
        {"check_same_thread": False}
        if SQLALCHEMY_DATABASE_URL.startswith("sqlite")
        else {}
    ),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
