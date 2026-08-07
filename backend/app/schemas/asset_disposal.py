from pydantic import BaseModel
from datetime import datetime


class DisposalRequest(BaseModel):
    asset_id: int
    reason: str


class DisposalApproval(BaseModel):
    approved_by: int


class DisposalResponse(BaseModel):
    disposal_id: int
    asset_id: int
    requested_by: int
    approved_by: int | None = None
    reason: str
    status: str
    requested_at: datetime
    approved_at: datetime | None = None

    class Config:
        from_attributes = True