from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    army_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.role_id"),
        nullable=False,
    )

    rank_id: Mapped[int] = mapped_column(
        ForeignKey("ranks.rank_id"),
        nullable=False,
    )

    unit_id: Mapped[int] = mapped_column(
        ForeignKey("units.unit_id"),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    last_login: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    role = relationship("Role")
    rank = relationship("Rank")
    unit = relationship("Unit")