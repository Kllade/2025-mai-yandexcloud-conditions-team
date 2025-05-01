from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Thread(BaseModel):
    user_id: int
    thread_id: str
    is_active: bool

class ThreadRead(Thread):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class ThreadCreate(Thread):
    pass


class ThreadFilter(BaseModel):
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    user_id: int | None = None
    thread_id: str | None = None
    is_active: bool | None = None
