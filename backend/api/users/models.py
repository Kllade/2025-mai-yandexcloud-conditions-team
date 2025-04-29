from api.core.base.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column
import enum
from sqlalchemy import Integer, Enum, ARRAY

class EducationType(enum.Enum):
    basic_higher="basic_higher"
    specialty="specialty"
    specialized_higher="specialized_higher"


class UsersOrm(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    tg_nick: Mapped[str]
    is_admin: Mapped[bool]
    request_count: Mapped[int]
    positive_count: Mapped[int]
    negative_count: Mapped[int]
    favorite_instituties: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=True)
    education_type: Mapped[EducationType] = mapped_column(Enum(EducationType, name="education_type_enum"), nullable=True)
    
    
    