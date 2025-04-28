from fastapi import APIRouter, Depends, Path, Body, Query, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import Annotated
from api.users.service import users_service

from api.core.session_manager import SessionDep, TransactionSessionDep
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["Results"])


# @router.get("/is_admin/{user_id}")
# async def is_admins(user_id: int, session: AsyncSession = SessionDep):
#     return await users_service.is_admin(session=session, user_id=user_id)
   