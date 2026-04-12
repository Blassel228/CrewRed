from pydantic import BaseModel


class TokenData(BaseModel):
    email: str


class TokenResponse(BaseModel):
    access_token: str
