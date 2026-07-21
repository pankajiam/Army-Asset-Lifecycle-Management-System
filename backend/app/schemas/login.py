from pydantic import BaseModel


class LoginRequest(BaseModel):
    army_number: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str