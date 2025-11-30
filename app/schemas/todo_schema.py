from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from typing import Optional


class TodoCreateSchema(BaseModel):
    user_id: int
    uuid: str = None  # UUID will be generated in service, so optional here
    title: str = Field(..., min_length=2)
    scheduled_date: date = Field(..., description="Date when todo is scheduled")
    priority: str = Field("low", description="Priority must be: low, medium, high")
    status: Optional[str] = Field("pending", description="Status: pending, in-progress, completed, hold, revoked")
    description: Optional[str] = None

    @field_validator("priority")
    def validate_priority(cls, validate):
        allowed = ["low", "medium", "high"]
        if validate not in allowed:
            raise ValueError(f"priority must be one of {allowed}")
        return validate
        

    @field_validator("status")
    def validate_status(cls, validate):
        allowed = ["pending", "in-progress", "completed", "hold", "revoked"]
        if validate not in allowed:
            raise ValueError(f"status must be one of {allowed}")
        return validate


class TodoUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=2)
    scheduled_date: Optional[date] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None

    @field_validator("priority")
    def validate_priority(cls, validate):
        if validate is None:
            return validate
        allowed = ["low", "medium", "high"]
        if validate not in allowed:
            raise ValueError(f"priority must be one of {allowed}")
        return validate

    @field_validator("status")
    def validate_status(cls, validate):
        if validate is None:
            return validate
        allowed = ["pending", "in-progress", "completed", "hold", "revoked"]
        if validate not in allowed:
            raise ValueError(f"status must be one of {allowed}")
        return validate


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
