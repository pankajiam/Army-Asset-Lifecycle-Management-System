from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    army_number: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str
    role_id: int
    rank_id: int
    unit_id: int

class UserResponse(BaseModel):
    user_id: int
    army_number: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str

    model_config = {
        "from_attributes": True
    }    