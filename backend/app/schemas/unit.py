from pydantic import BaseModel


class UnitResponse(BaseModel):

    unit_id: int
    unit_name: str
    location: str

    model_config = {
        "from_attributes": True
    }