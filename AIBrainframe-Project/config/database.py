from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

# Database configuration
# Environment-based database selection
USE_POSTGRES = config('USE_POSTGRES', default='false', cast=bool)

if USE_POSTGRES:
    # PostgreSQL for production
    DATABASE_URL = f"postgresql://{config('DB_USER', default='aibrainframe_user')}:{config('DB_PASSWORD', default='0320')}@{config('DB_HOST', default='localhost')}/{config('DB_NAME', default='aibrainframe_db')}"
    engine = create_engine(DATABASE_URL)
else:
    # SQLite for development/testing
    DATABASE_URL = "sqlite:///./aibrainframe.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()