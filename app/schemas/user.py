from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    surname: str
    password_hash: str = Field(..., min_length=8)
