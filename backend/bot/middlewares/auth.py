from __future__ import annotations
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
import logging

from api.users.service import users_service
from api.users.schemas import UserFilter, UserCreate
from bot.utils.command import find_command_argument

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram.types import TelegramObject
    from sqlalchemy.ext.asyncio import AsyncSession


logger = logging.getLogger(__name__)

class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)
    

        session: AsyncSession = data["session"]
        message: Message = event
        user = message.from_user

        if not user:
            return await handler(event, data)
        user = users_service.find_one_or_none(session=session, filters=UserFilter(id=user.id))
        if user:
            return await handler(event, data)

        referrer = find_command_argument(message.text)

        logger.info(f"new user registration | user_id: {user.id} | message: {message.text}")

        await users_service.add(session=session, values=UserCreate(tg_id=user.id, tg_nick=user.username, is_admin=False))

        return await handler(event, data)
