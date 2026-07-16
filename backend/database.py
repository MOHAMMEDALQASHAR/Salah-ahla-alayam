from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Connect to postgres. Use environment variable or default. 
# Changed default to sqlite to run instantly out-of-the-box
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ahla_alayam.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
