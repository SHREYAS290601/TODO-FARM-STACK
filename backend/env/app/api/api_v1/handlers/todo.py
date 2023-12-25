from fastapi import Depends, APIRouter
from app.models.todo_model import Todo
from app.schemas.todo_schema import ToDoCreate, TodoUpdate, ToDoOut
from app.models.user_model import User
from app.api.dependencies import user_deps
from app.services.todo_service import ToDoServices
from typing import List
from uuid import UUID

todo_router = APIRouter()


@todo_router.get(
    "/", summary="Get all the Todo for the User", response_model=List[ToDoOut]
)
async def all_dos(current_user: User = Depends(user_deps.get_current_user)):
    return await ToDoServices.get_all_todos(current_user)


@todo_router.post("/create", summary="Create Todos ", response_model=ToDoOut)
async def create_todo(
    data: ToDoCreate, user: User = Depends(user_deps.get_current_user)
):
    return await ToDoServices.create_do_per_user(user, data)


@todo_router.get("/{todo_id}", summary="Get todo by ID", response_model=ToDoOut)
async def retrive(todo_id: UUID, user: User = Depends(user_deps.get_current_user)):
    return await ToDoServices.get_do_by_id(todo_id, user)


@todo_router.put(
    "/{todo_id}/update", summary="Update a todo", response_model=List[Todo]
)
async def update(
    data: TodoUpdate, todo_id: UUID, user: User = Depends(user_deps.get_current_user)
):
    return await ToDoServices.update_todo(todo_id=todo_id, data=data, user=user)


@todo_router.delete("/{todo_id}/delete", summary="Delete a todo")
async def delete(todo_id: UUID, user: User = Depends(user_deps.get_current_user)):
    return await ToDoServices.delete_todo(todo_id=todo_id, user=user)
