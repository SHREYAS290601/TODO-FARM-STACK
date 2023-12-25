from pydantic import UUID4, BaseModel


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: UUID4 = (None,)
    exp: int = None
