from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRead(BaseModel):
    email: EmailStr
    name: str
    surname: str


class UserCreateIn(BaseModel):
    email: EmailStr
    name: str
    surname: str
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    surname: str
    hashed_password: str


class UserUpdateIn(BaseModel):
    email: Optional[EmailStr] | None = None
    name: Optional[str] | None = None
    surname: Optional[str] | None = None
    password: Optional[str] | None = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] | None = None
    name: Optional[str] | None = None
    surname: Optional[str] | None = None
    hashed_password: Optional[str] | None = None
