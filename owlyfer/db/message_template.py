from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class MessageTemplate(Base):
    __tablename__ = "message_templates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str]
    text: Mapped[str]
