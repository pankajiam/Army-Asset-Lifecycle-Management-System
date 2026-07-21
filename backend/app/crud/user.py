from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

def create_user(db: Session, user: UserCreate):
    db_user = User(
        army_number=user.army_number,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        password_hash=hash_password(user.password),
        role_id=user.role_id,
        rank_id=user.rank_id,
        unit_id=user.unit_id,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user_by_army_number(
    db: Session,
    army_number: str
):
    return (
        db.query(User)
        .filter(User.army_number == army_number)
        .first()
    )