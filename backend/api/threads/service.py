from api.threads.repo import ThreadsRepo
from api.threads.repo import threads_repo
from api.core.base.base_service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession


class ThreadsService(BaseService):
    def __init__(self, repository: ThreadsRepo):
        self.repository = repository
        super().__init__(repository=self.repository)



threads_service: ThreadsService = ThreadsService(repository=threads_repo)