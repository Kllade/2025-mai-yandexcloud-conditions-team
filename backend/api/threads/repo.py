from api.core.base.base_repository import BaseRepository
from api.threads.models import ThreadsOrm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class ThreadsRepo(BaseRepository):
    model = ThreadsOrm


threads_repo: ThreadsRepo = ThreadsRepo()  