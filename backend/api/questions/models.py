from api.core.base.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column
import enum
from sqlalchemy import Integer, Enum, ForeignKey



class QuestionsOrm(Base):
    __tablename__ = "questions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", ondelete="SET NULL"))
    question_text: Mapped[str] = mapped_column()
    message_id: Mapped[int] = mapped_column(nullable=False)
    
    
    
    
    
    
    
    