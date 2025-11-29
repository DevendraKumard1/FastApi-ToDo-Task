from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional


class TodoCreateSchema(BaseModel):
    user_id: int
    uuid: str = None  # UUID will be generated in service, so optional here
    title: str = Field(..., min_length=2)
    scheduled_date: date = Field(..., description="Date when todo is scheduled")
    priority: str = Field(..., description="Priority must be: low, medium, high")
    status: Optional[str] = Field("pending", description="Status: pending, in-progress, completed, revoked")
    description: Optional[str] = None

    @validator("priority")
    def validate_priority(cls, v):
        allowed = ["low", "medium", "high"]
        if v not in allowed:
            raise ValueError(f"priority must be one of {allowed}")
        return v

    @validator("status")
    def validate_status(cls, v):
        allowed = ["pending", "in-progress", "completed", "revoked"]
        if v not in allowed:
            raise ValueError(f"status must be one of {allowed}")
        return v


class TodoUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=2)
    scheduled_date: Optional[date] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None

    @validator("priority")
    def validate_priority(cls, v):
        if v is None:
            return v
        allowed = ["low", "medium", "high"]
        if v not in allowed:
            raise ValueError(f"priority must be one of {allowed}")
        return v

    @validator("status")
    def validate_status(cls, v):
        if v is None:
            return v
        allowed = ["pending", "in-progress", "completed", "revoked"]
        if v not in allowed:
            raise ValueError(f"status must be one of {allowed}")
        return v


class TodoResponse(BaseModel):
    id: int
    uuid: str
    user_id: int
    title: str
    scheduled_date: date
    priority: str
    status: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True
        from_attributes = True
