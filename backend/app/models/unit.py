from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Unit(Base):
    __tablename__ = "units"

    unit_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    unit_name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    location: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )