from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL
from database.models import Base

# =====================================================
# Engine
# =====================================================

engine = create_engine(
    DATABASE_URL,
    future=True,
    echo=False,
    pool_pre_ping=True,
)

# =====================================================
# Session Factory
# =====================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)

# =====================================================
# Initialize Database
# =====================================================


def init_db():
    """
    Create all database tables.
    """

    Base.metadata.create_all(bind=engine)


# =====================================================
# Session Context Manager
# =====================================================


@contextmanager
def get_session():
    """
    Database session context.

    Usage:

    with get_session() as db:
        ...
    """

    db = SessionLocal()

    try:

        yield db

        db.commit()

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()
