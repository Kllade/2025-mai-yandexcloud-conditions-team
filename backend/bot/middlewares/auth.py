from __future__ import annotations
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
import logging

from api.users.service import users_service
from api.users.schemas import UserFilter, UserCreate
from bot.utils.command import find_command_argument
from bot.core.config import settings

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram.types import TelegramObject
    from sqlalchemy.ext.asyncio import AsyncSession



logger = logging.getLogger(__name__)

from aiogram.types import Update, Message

class AuthMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict[str, Any]):
        # Проверяем, что event — это Update с message
        if isinstance(event, Update) and event.message:
            message: Message = event.message
            session: AsyncSession = data.get("session")
            
            if not session:
                return await handler(event, data)

            from_user = message.from_user
            if not from_user:
                return await handler(event, data)

            user = await users_service.find_one_or_none(
                session=session,
                filters=UserFilter(tg_id=from_user.id)
            )
            if user:
                return await handler(event, data)

            logger.info(f"Registering new user | user_id: {from_user.id} | message: {message.text}")

            await users_service.add(
                session=session,
                values=UserCreate(
                    tg_id=from_user.id,
                    tg_nick=from_user.username,
                    is_admin=str(from_user.id) in settings.ADMIN_IDS.split(","),
                    request_count=0,
                    positive_count=0,
                    negative_count=0,
                )
            )

        return await handler(event, data)


