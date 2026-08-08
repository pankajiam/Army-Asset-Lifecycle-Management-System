from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.crud.recent_activity import get_recent_activities
from app.schemas.recent_activity import RecentActivity

from app.models.user import User
from app.services.auth_service import get_current_user


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/recent-activities",
    response_model=list[RecentActivity]
)
def recent_activities(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_recent_activities(db)