import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .admin_post_state import AdminPostState


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str]
    state: Mapped[str]
    send_date: Mapped[datetime.datetime]
    notification: Mapped[bool]

    user: Mapped["User"] = relationship(back_populates="posts")
    admin_states: Mapped[List["AdminPostState"]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan",
    )
