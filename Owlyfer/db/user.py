from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .post import Post


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int]
    ban_state: Mapped[bool] = mapped_column(default=False)

    posts: Mapped["Post"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
