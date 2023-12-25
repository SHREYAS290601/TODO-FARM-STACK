from fastapi import Body, status, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from app.schemas import auth_schema, user_schema
from app.services.user_service import UserServices
from app.core.security import create_access_token, create_refresh_access_token
from app.api.dependencies import user_deps
from app.models.user_model import User
from app.schemas.auth_schema import TokenPayload
from datetime import datetime
from pydantic import ValidationError
from jose.jwt import JWTError
from app.core.config import settings
from jose import jwt
auth_router = APIRouter()


@auth_router.post(
    "/login",
    summary="Authenticate and create JWT token",
    response_model=auth_schema.TokenSchema,
)
async def login(data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserServices.authenticate(email=data.username, password=data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_UNAUTHORIZED,
            detail="No user found!Cannot Login",
        )
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_access_token(user.user_id),
    }


@auth_router.post(
    "/test_token",
    summary="Token testing for a User",
    response_model=user_schema.UserOutPut,
)
async def test_token(user: User = Depends(user_deps.get_current_user)):
    return user


@auth_router.post(
    "/refresh", summary="Refresh the token", response_model=auth_schema.TokenSchema
)
async def refresh_token(refresh_token: str = Body(...)):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        token_data = TokenPayload(**payload)

        # if datetime.fromtimestamp(token_data.exp) < datetime.now():
        #     raise HTTPException(
        #         status_code=status.HTTP_401_BAD_REQUEST,
        #         description="Token Expired",
        #         headers={"WWW-Authenticate": "Bearer"},
        #     )
    except (JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            descripton="Could not Validate",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await UserServices.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            desciption="User could not be found with the given ID",
        )
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_access_token(user.user_id),
    }
