from api.questions.repo import QuestionsRepo
from api.questions.repo import questions_repo
from api.core.base.base_service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession


class QuestionsService(BaseService):
    def __init__(self, repository: QuestionsRepo):
        self.repository = repository
        super().__init__(repository=self.repository)



questions_service: QuestionsService = QuestionsService(repository=questions_repo)