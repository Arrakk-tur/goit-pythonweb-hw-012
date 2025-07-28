from datetime import date
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum


# Contacts
class ContactBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    phone: str
    birthday: date
    extra_data: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int

    class Config:
        from_attributes = True

# User
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    role: RoleEnum
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True

class LoginModel(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
