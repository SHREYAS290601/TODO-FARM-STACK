from beanie import Document, Indexed, Link, Replace, Insert,before_event
from pydantic import Field, EmailStr 
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from .user_model import User


class Todo(Document):
    todo_id: UUID = Field(default_factory=uuid4, unique=True)
    status: bool = False
    title: Indexed(str)
    description: str = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    owner: Link[User]

    def __repr__(self) -> str:
        return f"Todo was {self.title}"

    def __str__(self) -> str:
        return f"{self.todo_id}"

    def __hash__(self) -> int:
        return hash(self.title)

    def __eq__(self, other: object) -> bool:
        return self.todo_id == other.todo_id if isinstance(other, Todo) else False

    @before_event([Replace, Insert])
    def update_updateed_at(self):
        self.updated_at = datetime.utcnow()

    class Settings:
        name = "todo"
    
    class Config:
        arbitrary_types_allowed=True


