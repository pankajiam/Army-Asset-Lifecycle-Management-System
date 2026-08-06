from sqlalchemy.orm import Session

from app.models.asset_category import AssetCategory


def get_asset_categories(db: Session):

    return (
        db.query(AssetCategory)
        .order_by(AssetCategory.category_name)
        .all()
    )