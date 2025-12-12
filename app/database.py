from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings 

settings = get_settings()

SQLALCHAMY_DATABASE_URL = (
    f"mysql+pymysql://{settings.MYSQLUSER}:{settings.MYSQLPASSWORD}"
    f"@{settings.MYSQLHOST}:{settings.MYSQLPORT}/{settings.MYSQLDATABASE}"
)

engine = create_engine(SQLALCHAMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
