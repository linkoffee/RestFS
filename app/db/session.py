from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings_v1

engine = create_engine(
    settings_v1.DB_URL,
    connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# dependency for getting db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
