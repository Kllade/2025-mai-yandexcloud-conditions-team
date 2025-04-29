from api.core.base.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column
import enum
from sqlalchemy import Integer, Enum, ForeignKey



class QuestionsOrm(Base):
    __tablename__ = "questions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    question_text: Mapped[str] = mapped_column(unique=True)
    message_id: Mapped[int]
    
    def __repr__(self):
        return f"<Question(id={self.id}, user_id={self.user_id}, text={self.question_text[:50]}...)>" 
    
    
    
    
    
    