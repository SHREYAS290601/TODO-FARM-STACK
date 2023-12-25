from typing import Optional, List
import pymongo
from fastapi import status, HTTPException
from pydantic import UUID4
from uuid import UUID
from app.models.user_model import User
from app.models.todo_model import Todo
from app.schemas.todo_schema import ToDoCreate, TodoUpdate, ToDoOut


class ToDoServices:
    @staticmethod
    async def get_all_todos(user: User) -> List[Todo]:
        todos = await Todo.find(Todo.owner.id == user.id).to_list()
        return todos

    @staticmethod
    async def create_do_per_user(user: User, data: ToDoCreate) -> Todo:
        todo = Todo(
            **data.dict(),
            owner=user,
        )
        await todo.insert()
        return todo

    @staticmethod
    async def get_do_by_id(todo_id: UUID, user: User) -> List[Todo]:
        todo = await Todo.find_one(Todo.todo_id == todo_id, Todo.owner.id == user.id)
        if todo:
            return todo
        else:
            mydo = await Todo.find_one(Todo.todo_id == todo_id)
            if not mydo:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="NO TODO BY THAT ID"
                )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No todo found by the id",
            )

    @staticmethod
    async def update_todo(todo_id: UUID, user: User, data: TodoUpdate):
        todo = await ToDoServices.get_do_by_id(todo_id=todo_id, user=user)
        await todo.update({"$set": data.dict(exclude_unset=True)})

        await todo.save()
        return todo

    @staticmethod
    async def delete_todo(todo_id: UUID, user: User):
        todo = await ToDoServices.get_do_by_id(todo_id, user)
        if todo:
            await todo.delete()
        return None
