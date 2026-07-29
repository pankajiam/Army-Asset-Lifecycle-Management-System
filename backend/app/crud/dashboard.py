from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.asset import Asset
from app.models.asset_disposal import AssetDisposal


def get_dashboard_summary(db: Session):

    total_assets = (
        db.query(func.count(Asset.asset_id))
        .scalar()
    )

    assigned_assets = (
        db.query(func.count(Asset.asset_id))
        .filter(Asset.assigned_to.isnot(None))
        .scalar()
    )

    available_assets = (
        db.query(func.count(Asset.asset_id))
        .filter(Asset.status == "Available")
        .scalar()
    )

    disposed_assets = (
        db.query(func.count(Asset.asset_id))
        .filter(Asset.status == "Disposed")
        .scalar()
    )

    pending_disposals = (
        db.query(func.count(AssetDisposal.disposal_id))
        .filter(AssetDisposal.status == "Pending")
        .scalar()
    )

    return {
        "total_assets": total_assets,
        "assigned_assets": assigned_assets,
        "available_assets": available_assets,
        "disposed_assets": disposed_assets,
        "pending_disposals": pending_disposals
    }