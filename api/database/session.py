from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./data/scoring.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # obligatoire pour SQLite
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
