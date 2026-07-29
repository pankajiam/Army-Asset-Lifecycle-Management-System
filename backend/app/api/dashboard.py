from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.crud.dashboard import get_dashboard_summary
from app.schemas.dashboard import DashboardSummary


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/summary",
    response_model=DashboardSummary
)
def dashboard_summary(
    db: Session = Depends(get_db)
):
    return get_dashboard_summary(db)