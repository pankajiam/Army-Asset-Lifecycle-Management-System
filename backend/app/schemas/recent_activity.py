from datetime import datetime
from pydantic import BaseModel


class RecentActivity(BaseModel):
    audit_id: int
    action: str
    remarks: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True