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
    favorite_instituties: list[int] | None = None
    education_type: EducationType | None = None

class UserRead(User):
    id: int
    created_at: datetime
    updated_at: datetime


class UserCreate(User):
    pass


class UserFilter(BaseModel):
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    tg_id: int | None = None
    tg_nick: str | None = None
    is_admin: bool | None = None
    request_count: int | None = None
    positive_count: int | None = None
    negative_count: int | None = None
    favorite_instituties: list[int] | None = None
    education_type: EducationType | None = None