import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Build connection string safely
oracle_user = os.getenv("ORACLE_USER", "smart_expense")
oracle_password = os.getenv("ORACLE_PASSWORD", "Oracle123")
oracle_host = os.getenv("ORACLE_HOST", "localhost")
oracle_port = os.getenv("ORACLE_PORT", "1521")
oracle_service = os.getenv("ORACLE_SERVICE_NAME", "XEPDB1")

# URL-encode password in case of special characters like '#'
encoded_password = urllib.parse.quote_plus(oracle_password)

default_db_url = f"oracle+oracledb://{oracle_user}:{encoded_password}@{oracle_host}:{oracle_port}/?service_name={oracle_service}"
DATABASE_URL = os.getenv("DATABASE_URL", default_db_url)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that provides a database session and safely closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
