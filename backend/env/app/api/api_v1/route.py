from fastapi import APIRouter
from app.api.api_v1.handlers import user,todo
from app.api.auth import jwt
router = APIRouter()
router.include_router(user.user_router, prefix="/user", tags=["User"])
router.include_router(jwt.auth_router, prefix="/auth", tags=["Auth"])
router.include_router(todo.todo_router, prefix="/todo", tags=["ToDo"])
