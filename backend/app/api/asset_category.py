from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.asset_category import AssetCategoryResponse

from app.crud.asset_category import get_asset_categories


router = APIRouter(
    prefix="/asset-categories",
    tags=["Asset Categories"],
)


@router.get(
    "/",
    response_model=list[AssetCategoryResponse]
)
def read_asset_categories(
    db: Session = Depends(get_db)
):

    return get_asset_categories(db)