from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Question(BaseModel):
    user_id: int
    question_text: str
    message_id: int

class QuestionRead(Question):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class QuestionCreate(Question):
    pass


class QuestionFilter(BaseModel):
    id: int 
    created_at: datetime 
    updated_at: datetime 
    user_id: int
    question_text: str
    message_id: int
