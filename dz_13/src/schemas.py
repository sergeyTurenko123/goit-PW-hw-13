from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

class ContactBase(BaseModel):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email_address: str = Field(max_length=50)
    phone_number: str = Field(max_length=50)
    date_of_birth: date
    additional_data: str = Field(max_length=150)

class ContactStatusUpdate(BaseModel):
    done: bool

class ContactResponse(ContactBase):
    id: int
    created_at: datetime

    class ConfigDict:
        orm_mode = True

class UserModel(BaseModel):
    username: str = Field(min_length=4, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class ConfigDict:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    email: EmailStr
