from pydantic import BaseModel


class RoleResponse(BaseModel):

    role_id: int
    role_name: str
    description: str | None = None

    model_config = {
        "from_attributes": True
    }