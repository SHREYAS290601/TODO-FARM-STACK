from pydantic import UUID4, BaseModel,EmailStr,Field
from typing import Optional
class UserAuth(BaseModel):
    email:EmailStr=Field(...,description="User email")
    username:str=Field(...,min_length=5,max_length=50,description="Username create")
    password:str=Field(...,min_length=5,max_length=50,description="Password")
    
class UserOutPut(BaseModel):
    user_id:UUID4
    username:str
    email:EmailStr
    first_name:Optional[str]
    last_name:Optional[str]

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None