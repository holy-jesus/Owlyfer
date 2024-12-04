from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .admin_post_state import AdminPostState


class Admin(Base):
    __tablename__ = "admin"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int]
    nickname: Mapped[str]

    post_states: Mapped["AdminPostState"] = relationship(
        back_populates="admin",
        cascade="all, delete-orphan",
    )
