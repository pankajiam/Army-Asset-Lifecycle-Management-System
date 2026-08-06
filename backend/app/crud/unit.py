from sqlalchemy.orm import Session

from app.models.unit import Unit


def get_units(db: Session):

    return (
        db.query(Unit)
        .order_by(Unit.unit_name)
        .all()
    )