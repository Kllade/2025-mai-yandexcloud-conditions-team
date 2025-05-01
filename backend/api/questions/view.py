from fastapi import APIRouter, Depends, Path, Body, Query, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import Annotated
from api.questions.service import questions_service
from api.core.session_manager import SessionDep, TransactionSessionDep
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("/all_text")
async def get_all(session: AsyncSession = SessionDep):
    return await questions_service.get_all_questions_text(session=session)
   

