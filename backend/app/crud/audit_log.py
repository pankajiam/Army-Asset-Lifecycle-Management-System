from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    user_id: int,
    action: str,
    asset_id: int | None = None,
    remarks: str | None = None
):
    log = AuditLog(
        user_id=user_id,
        asset_id=asset_id,
        action=action,
        remarks=remarks
    )

    db.add(log)
    

    return log