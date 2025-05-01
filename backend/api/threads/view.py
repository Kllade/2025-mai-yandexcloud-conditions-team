from fastapi import APIRouter, Depends, Path, Body, Query, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import Annotated
from api.threads.service import threads_service
from bot.handlers.on_click.main_menu import on_support
from api.core.session_manager import SessionDep, TransactionSessionDep
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/threads", tags=["Threads"])


@router.get("")
async def get_all(session: AsyncSession = SessionDep):
    return await threads_service.find_all(session=session)
   

