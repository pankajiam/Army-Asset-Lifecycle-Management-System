from pydantic import BaseModel


class RankResponse(BaseModel):

    rank_id: int
    rank_name: str
    level: int
    can_approve: bool

    model_config = {
        "from_attributes": True
    }