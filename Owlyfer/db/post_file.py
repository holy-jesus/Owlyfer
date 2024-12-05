from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class PostFile(Base):
    __tablename__ = "post_file"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    post_id: Mapped[int]
    file_type: Mapped[str]
    file_id: Mapped[str]
