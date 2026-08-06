from pydantic import BaseModel


class AssetStatusResponse(BaseModel):

    status_id: int
    status_name: str
    description: str | None = None

    model_config = {
        "from_attributes": True
    }