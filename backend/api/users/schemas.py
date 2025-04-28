from pydantic import BaseModel, ConfigDict
from api.users.models import EducationType
from datetime import datetime

class User(BaseModel):
    tg_id: int
    tg_nick: str
    is_admin: bool
    request_count: int
    positive_count: int
    negative_count: int
    favorite_instituties: list[int]
    education_type: EducationType

class UserRead(User):
    id: int
    created_at: datetime
    updated_at: datetime


class UserCreate(User):
    pass


class UserFilter(BaseModel):
    id: int 
    created_at: datetime 
    updated_at: datetime 
    tg_id: int
    tg_nick: str
    is_admin: bool
    request_count: int | None = None
    positive_count: int | None = None
    negative_count: int | None = None
    favorite_instituties: list[int] | None = None
    education_type: EducationType | None = None