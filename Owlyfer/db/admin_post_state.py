from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .admin import Admin
    from .post import Post


class AdminPostState(Base):
    __tablename__ = "admin_post_state"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message_id: Mapped[int]

    admin_id: Mapped[int] = mapped_column(ForeignKey("admin.id"))
    admin: Mapped["Admin"] = relationship(back_populates="post_states")

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="admin_states")
