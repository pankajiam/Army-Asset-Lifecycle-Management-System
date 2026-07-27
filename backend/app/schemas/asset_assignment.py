from pydantic import BaseModel
from datetime import datetime


class AssetIssue(BaseModel):
    asset_id: int
    user_id: int
    issue_condition: str = "Good"


class AssignmentResponse(BaseModel):
    assignment_id: int
    asset_id: int
    user_id: int
    issue_condition: str
    return_condition: str | None = None
    returned_at: datetime | None = None

    class Config:
        from_attributes = True

class AssetReturn(BaseModel):
    asset_id: int
    return_condition: str = "Good"

class AssetTransfer(BaseModel):
    asset_id: int
    new_user_id: int
    transfer_condition: str = "Good"