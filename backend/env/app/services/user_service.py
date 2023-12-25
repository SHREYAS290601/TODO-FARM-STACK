from app.schemas.user_schema import UserAuth
from app.models.user_model import User
from app.core.security import get_password, verify_password
from typing import Optional
import pymongo
from fastapi import status, HTTPException
from pydantic import EmailStr, UUID4
from app.models.user_model import User
from app.schemas.user_schema import UserUpdate


class UserServices:
    @staticmethod
    async def create_user(user: UserAuth):
        flag=await User.find_one(User.email==user.email)
        if not flag:
            user_in = User(
                username=user.username,
                email=user.email,
                hashed_password=get_password(user.password),
            )
            await user_in.save()
            return user_in
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User with the email already exits"
            )

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        return user

    @staticmethod
    async def get_user_by_id(id: UUID4) -> Optional[User]:
        user = await User.find_one(User.user_id == id)
        return user

    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        try:
            user = await UserServices.get_user_by_email(email=email)
            if not user:
                return None
            if not verify_password(password=password, hashed_pass=user.hashed_password):
                return None

            return user
        except pymongo.errors.OperationFailure:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The email is not found! Check the email again or use the one with which you have registered.",
            )

    @staticmethod
    async def user_info(email: str, user: User):
        current_user = await User.find_one(User.email == email, User.id == user.id)
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found by that email",
            )
        return await current_user

    @staticmethod
    async def update_user(data: UserUpdate, email: EmailStr, user: User):
        current_user = await User.find_one(User.email == email, User.id == user.id)
        if current_user:
            await current_user.update({"$set": data.dict(exclude_unset=True)})

            await current_user.save()
            return current_user
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found or the email was wrong!Please check",
            )

    @staticmethod
    async def delete_the_user(email: EmailStr, user: User):
        current_user = await User.find_one(User.email == email, User.id == user.id)
        if current_user:
            await current_user.delete()
            return None
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found or the email was wrong!Please check",
        )
