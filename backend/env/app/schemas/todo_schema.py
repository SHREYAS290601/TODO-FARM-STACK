from app.models.todo_model import Todo
from app.models.user_model import User
from pydantic import UUID4, BaseModel, Field
from typing import Optional
from datetime import datetime


class ToDoCreate(BaseModel):
    title: str = Field(..., title="Title", max_length=100, min_length=1)
    description: str = Field(..., title="Describe", max_length=300, min_length=1)
    status: Optional[bool] = False


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(..., title="Title", max_length=100, min_length=1)
    description: Optional[str] = Field(
        ..., title="Describe", max_length=100, min_length=1
    )
    status: Optional[bool] = False


class ToDoOut(BaseModel):
    todo_id: UUID4
    status: bool
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
