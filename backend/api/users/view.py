from fastapi import APIRouter, Depends, Path, Body, Query, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import Annotated
from api.users.service import users_service

from api.core.session_manager import SessionDep, TransactionSessionDep
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["Results"])


@router.get("")
async def get_all(session: AsyncSession = SessionDep):
    return await users_service.find_all(session=session)
   