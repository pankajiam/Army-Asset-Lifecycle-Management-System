from sqlalchemy.orm import Session

from app.models.rank import Rank


def get_ranks(db: Session):

    return (
        db.query(Rank)
        .order_by(Rank.level)
        .all()
    )