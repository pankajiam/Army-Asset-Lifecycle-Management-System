from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def get_recent_activities(db: Session):

    activities = (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .limit(10)
        .all()
    )

    return activities