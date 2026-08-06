from pydantic import BaseModel


class AssetCategoryResponse(BaseModel):

    category_id: int
    category_name: str
    description: str | None = None

    model_config = {
        "from_attributes": True
    }