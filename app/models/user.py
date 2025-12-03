from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(CHAR(36), unique=True, nullable=False)
    username = Column(String(50), unique=False, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(500), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    todos = relationship("Todo", back_populates="user")