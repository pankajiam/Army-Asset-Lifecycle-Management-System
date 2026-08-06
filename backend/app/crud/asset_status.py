from sqlalchemy.orm import Session

from app.models.asset_status import AssetStatus


def get_asset_statuses(db: Session):

    return (
        db.query(AssetStatus)
        .order_by(AssetStatus.status_name)
        .all()
    )