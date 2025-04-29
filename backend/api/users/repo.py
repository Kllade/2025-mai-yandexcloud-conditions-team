from api.core.base.base_repository import BaseRepository
from api.users.models import UsersOrm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

class UsersRepo(BaseRepository):
    model = UsersOrm


    async def is_admin(self, session: AsyncSession, user_id: int):
        query = select(UsersOrm).where(UsersOrm.id == user_id)
        result = await session.execute(query)
        result = result.scalar_one_or_none()
        if result:
            return result.is_admin
        return False
    
    async def get_all_admins(self, session: AsyncSession):
        query = select(UsersOrm).where(UsersOrm.is_admin == True)
        result = await session.execute(query)
        result = result.scalars()
        if result:
            return result
        return []
    
    async def update_reaction_stats(self, session: AsyncSession, user_id: int, is_helpful: bool, remove: bool = False) -> None:
        """Update user's reaction statistics
        
        Args:
            user_id: Telegram user ID
            is_helpful: Whether the reaction was helpful (True for 👍, False for 👎)
            remove: Whether this is a reaction removal (True) or addition (False)
        """
        if is_helpful:
            query = await update(UsersOrm.positive_count).where(UsersOrm.tg_id == user_id).values(positive_count=UsersOrm.positive_count + 1 if not remove else UsersOrm.positive_count - 1).execution_options(synchronize_session=False)
        else:
            query = await update(UsersOrm.negative_count).where(UsersOrm.tg_id == user_id).values(negative_count=UsersOrm.negative_count + 1 if not remove else UsersOrm.negative_count - 1).execution_options(synchronize_session=False)
        
        await session.execute(query)
        await session.commit()



users_repo: UsersOrm = UsersRepo()