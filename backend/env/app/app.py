from fastapi import FastAPI
from app.core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user_model import User
from app.models.todo_model import Todo
from app.api.api_v1.route import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def app_init():
    """
    Initialize the crucial Application services

    """
    db_client = AsyncIOMotorClient(settings.MONGODB_CONNECTION_STRING).letsdoit

    await init_beanie(
        database=db_client,
        document_models=[User, Todo],
    )
    app.include_router(router=router, prefix=settings.API_V1_STR)
