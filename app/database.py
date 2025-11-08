from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHAMY_DATABASE_URL = "mysql+pymysql://root@localhost:3306/todo_db"

engine = create_engine(SQLALCHAMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def register_models():
    import app.schemas.User
    import app.schemas.ToDo
