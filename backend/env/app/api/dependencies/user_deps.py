from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from fastapi import HTTPException, Depends, status
from app.models.user_model import User
from jose import jwt
from app.schemas.auth_schema import TokenPayload
from datetime import datetime
from pydantic import ValidationError
from jose.jwt import JWTError
from app.services.user_service import UserServices

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login", scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth)) -> User:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_BAD_REQUEST,
                detail="Token Expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not Validate",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await UserServices.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User could not be found with the given ID",
        )
    return user
