from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional

class ToDoCreateSchema(BaseModel):
    user_id: int
    title: str
    scheduled_date: date = Field(..., description="Date when todo is scheduled")
    priority: str = Field(..., description="Priority of todo: low, medium, high")
    status: Optional[str] = Field("pending", description="Status of the todo")
    description: Optional[str] = Field(None, description="Optional description")


class TodoResponse(BaseModel):
    id: int
    uuid: str
    user_id: str
    title: str
    scheduled_date: date
    priority: str
    status: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }