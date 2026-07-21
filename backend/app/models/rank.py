from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Rank(Base):
    __tablename__ = "ranks"

    rank_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    rank_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    level: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    can_approve: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )