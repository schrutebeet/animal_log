# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from credentials import DatabaseKey
# Replace with your actual database credentials
SQLALCHEMY_DATABASE_URL = f"postgresql://{DatabaseKey.user}:{DatabaseKey.password}@{DatabaseKey.host}/{DatabaseKey.database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Dependency for getting DB session in routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
