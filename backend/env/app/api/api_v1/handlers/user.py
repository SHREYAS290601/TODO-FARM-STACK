from fastapi import status, HTTPException, APIRouter, Depends
from app.schemas import user_schema
from app.services.user_service import UserServices
import pymongo
import logging
from app.models.user_model import User
from app.api.dependencies.user_deps import get_current_user


user_router = APIRouter()
us = UserServices()


@user_router.post(
    "/create", summary="Create a new user", response_model=user_schema.UserOutPut
)
async def create_new_user(data: user_schema.UserAuth):
    try:
        return await us.create_user(data)
    except pymongo.errors.DuplicateKeyError as e:
        print(f"Error was {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="User with this email already exits!Please enter another email id",
        )
    finally:
        logging.info("User creation done")


@user_router.get(
    "/user", summary="User Information", response_model=user_schema.UserOutPut
)
async def user_information(user: User = Depends(get_current_user)):
    return user


@user_router.put(
    "/update", summary="Update the user", response_model=user_schema.UserOutPut
)
async def update(
    data: user_schema.UserUpdate, email: str, user: User = Depends(get_current_user)
):
    return await us.update_user(data, email, user)


@user_router.delete("/delete", summary="Delete a user")
async def delete_user(email: str, user: User = Depends(get_current_user)):
    if user.email==email:
        return await us.delete_the_user(email, user)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Method not allowed!"
    )
