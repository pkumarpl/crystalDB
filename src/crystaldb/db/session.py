"""Database session configuration and management."""

from collections.abc import Generator
from typing import Any

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

from ..core.config import get_settings
from ..core.logging import get_logger
from .base import Base

logger = get_logger(__name__)
settings = get_settings()

# Create engine with appropriate settings for database type
is_sqlite = settings.database_url.startswith("sqlite")
engine_kwargs = {
    "echo": settings.is_development,  # SQL logging in development
}

# SQLite-specific settings
if is_sqlite:
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    # MySQL/PostgreSQL pooling settings
    engine_kwargs.update({
        "poolclass": QueuePool,
        "pool_size": 5,
        "max_overflow": 10,
        "pool_pre_ping": True,
        "pool_recycle": 3600,
    })

engine = create_engine(settings.database_url, **engine_kwargs)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@event.listens_for(Engine, "connect")
def set_mysql_pragma(dbapi_conn: Any, connection_record: Any) -> None:
    """Set MySQL connection options."""
    # Only set MySQL-specific options for MySQL databases
    if not is_sqlite:
        try:
            cursor = dbapi_conn.cursor()
            cursor.execute("SET SESSION sql_mode='STRICT_TRANS_TABLES'")
            cursor.close()
        except Exception:
            pass  # Skip if not MySQL


def init_db() -> None:
    """Initialize database by creating all tables."""
    try:
        # Import all models to ensure they're registered
        from ..models import (  # noqa: F401
            User,
            Material,
            Solvent,
            Experiment,
            Morphology,
            Measurement,
        )

        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def get_db() -> Generator[Session, None, None]:
    """Dependency for getting database session.

    Yields:
        Database session

    Example:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
