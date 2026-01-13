from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    role: Optional[str]

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True



# from pydantic import BaseModel, EmailStr, Field
# from datetime import datetime

# class UserCreate(BaseModel):
#     username: str
#     email: EmailStr
#     password: str = Field(
#         min_length=8,
#         max_length=64,  # 👈 clave
#         description="Password entre 8 y 64 caracteres"
#     )


# class UserOut(BaseModel):
#     id: int
#     username: str
#     email: EmailStr
#     created_at: datetime

#     class Config:
#         from_attributes = True
