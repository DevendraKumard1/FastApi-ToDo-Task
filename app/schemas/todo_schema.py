from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError
from datetime import date, datetime
from typing import Optional


# ---------------------------
# CREATE
# ---------------------------
class TodoCreateSchema(BaseModel):
    user_id: int
    title: str = Field(..., min_length=2)
    scheduled_date: date
    priority: str = Field("low")
    status: str = Field("pending")
    description: Optional[str] = None

    @field_validator("priority")
    def validate_priority(cls, v):
        allowed = ["low", "medium", "high"]
        if v not in allowed:
            raise PydanticCustomError(
                "priority.invalid",
                f"Priority must be one of {allowed}"
            )
        return v

    @field_validator("status")
    def validate_status(cls, v):
        allowed = ["pending", "in_progress", "completed", "hold", "revoked"]
        if v not in allowed:
            raise PydanticCustomError(
                "status.invalid",
                f"Status must be one of {allowed}"
            )
        return v


# ---------------------------
# UPDATE
# ---------------------------
class TodoUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=2)
    scheduled_date: Optional[date] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None

    @field_validator("priority")
    def validate_priority(cls, v):
        if v is None:
            return v
        allowed = ["low", "medium", "high"]
        if v not in allowed:
            raise PydanticCustomError(
                "priority.invalid",
                f"Priority must be one of {allowed}"
            )
        return v

    @field_validator("status")
    def validate_status(cls, v):
        if v is None:
            return v
        allowed = ["pending", "in_progress", "completed", "hold", "revoked"]
        if v not in allowed:
            raise PydanticCustomError(
                "status.invalid",
                f"Status must be one of {allowed}"
            )
        return v


# ---------------------------
# RESPONSE
# ---------------------------
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
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    model_config = {"from_attributes": True}
