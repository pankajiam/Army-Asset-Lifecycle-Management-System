from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.audit_log import AuditLog
from app.models.user import User

from app.schemas.audit_log import AuditLogResponse

from app.services.auth_service import require_admin_or_co


router = APIRouter(
    prefix="/audit",
    tags=["Audit Logs"]
)


@router.get(
    "/",
    response_model=list[AuditLogResponse]
)
def get_all_logs(
    current_user: User = Depends(require_admin_or_co),
    db: Session = Depends(get_db)
):
    return (
        db.query(AuditLog)
        .order_by(
            AuditLog.created_at.desc()
        )
        .all()
    )