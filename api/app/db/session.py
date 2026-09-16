from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from api.app.config import settings

engine = create_engine(
    settings.niyam_db_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.niyam_db_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency for obtaining a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
