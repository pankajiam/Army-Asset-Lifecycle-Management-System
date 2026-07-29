from datetime import datetime
from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    audit_id: int
    user_id: int
    asset_id: int | None
    action: str
    remarks: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }