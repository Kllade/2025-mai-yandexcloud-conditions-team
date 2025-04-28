from __future__ import annotations
from typing import TYPE_CHECKING
from api.users.service import users_service
from api.core.session_manager import session_manager

from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat

if TYPE_CHECKING:
    from aiogram import Bot

users_commands: dict[str, dict[str, str]] = {
    "en": {
        "help": "help",
        "contacts": "developer contact details",
        "menu": "main menu with earning schemes",
        "supports": "support contacts",
    },
    "uk": {
        "help": "help",
        "contacts": "developer contact details",
        "menu": "main menu with earning schemes",
        "supports": "support contacts",
    },
    "ru": {
        "help": "help",
        "contacts": "developer contact details",
        "menu": "main menu with earning schemes",
        "supports": "support contacts",
    },
}

admins_commands: dict[str, dict[str, str]] = {
    "en": {
        "ping": "Check bot ping",
        "stats": "Show bot stats",
        "admin_menu": "menu for admin",
        "menu": "main menu with earning schemes",
        "support": "test"
    },
    "uk": {
        "ping": "Check bot ping",
        "stats": "Show bot stats",
        "admin_menu": "menu for admin",
        "menu": "main menu with earning schemes",
        "support": "test"
    },
    "ru": {
        "ping": "Check bot ping",
        "stats": "Show bot stats",
        "admin_menu": "menu for admin",
        "menu": "main menu with earning schemes",
        "support": "test"
    },
}


async def set_default_commands(bot: Bot) -> None:
    await remove_default_commands(bot)

    for language_code, commands in users_commands.items():
        await bot.set_my_commands(
            [BotCommand(command=command, description=description) for command, description in commands.items()],
            scope=BotCommandScopeDefault(),
            language_code=language_code,
        )

        async with session_manager.get_db_with_transaction() as session:
            admins = await users_service.get_all_admins(session)
        for admin in admins:
            
            await bot.set_my_commands(
                [
                    BotCommand(command=command, description=description)
                    for command, description in admins_commands[language_code].items()
                ],
                scope=BotCommandScopeChat(chat_id=admin.id),
            )


async def remove_default_commands(bot: Bot) -> None:
    await bot.delete_my_commands(scope=BotCommandScopeDefault())
