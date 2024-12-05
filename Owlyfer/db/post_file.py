from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .post import Post


class PostFile(Base):
    __tablename__ = "post_file"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="files")

    file_type: Mapped[str]
    file_id: Mapped[str]
