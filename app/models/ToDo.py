from sqlalchemy import Column, Integer, String, Text, Date, DateTime, func
from sqlalchemy.dialects.mysql import CHAR
from app.database import Base

class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(CHAR(36), unique=True, nullable=False)
    user_id = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    scheduled_date = Column(Date, nullable=False)
    priority = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)