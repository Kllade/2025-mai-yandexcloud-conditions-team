from api.core.base.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column
import enum
from sqlalchemy import Integer, Enum, ARRAY, BigInteger, Boolean, ForeignKey, String




class ThreadsOrm(Base):
    __tablename__ = "threads"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.tg_id"), nullable=False)
    thread_id: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)