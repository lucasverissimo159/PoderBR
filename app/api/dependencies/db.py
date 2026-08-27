from collections.abc import Generator

from app.db.session import SessionLocal


def get_db() -> Generator:
    """Dependency to inject database sessions into FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
