from api.core.base.base_repository import BaseRepository
from api.questions.models import QuestionsOrm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class QuestionsRepo(BaseRepository):
    model = QuestionsOrm



questions_repo: QuestionsOrm = QuestionsRepo()  