from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import DB_TYPE, SQLITE_PATH, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB


# =====================================================
# DB URL 생성
# =====================================================

def get_db_url():

    if DB_TYPE == "sqlite":
        return f"sqlite:///{SQLITE_PATH}"

    elif DB_TYPE == "postgres":

        return (
            f"postgresql+psycopg2://"
            f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
            f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        )

    else:
        raise ValueError(f"Unsupported DB_TYPE: {DB_TYPE}")


# =====================================================
# ENGINE
# =====================================================

engine = create_engine(
    get_db_url(),
    pool_pre_ping=True,
    echo=False
)


# =====================================================
# SESSION
# =====================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# =====================================================
# BASE MODEL
# =====================================================

Base = declarative_base()


# =====================================================
# DEPENDENCY
# =====================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
