from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.enums import ContentType
from bot.dialogs.main_menu.states import MainMenu
from aiogram_dialog import DialogManager, StartMode
from bot.handlers.on_click.main_menu import process_question, on_support
from aiogram.fsm.context import FSMContext
from bot.keyboards.inline_menu import main_menu_kb, support_kb
from sqlalchemy.ext.asyncio import AsyncSession
from api.cache.redis import redis_client, set_redis_value
from bot.core.loader import bot
from bot.keyboards.admin import main_menu_kb
from api.users.service import users_service
import logging
from api.users.schemas import UserFilter
logger = logging.getLogger(__name__)

router = Router(name="admin")

@router.message(Command("admin"))
async def admin_panel(message: types.Message, state: FSMContext, session: AsyncSession):
    """Обработчик команды /admin - показывает админскую панель"""
    user_id = message.from_user.id
    is_admin = await users_service.is_admin(session, user_id)
    
    if not is_admin:
        await message.answer("У вас нет доступа к админской панели.")
        return
        
    await message.answer(
        "Админская панель",
        reply_markup=main_menu_kb()
    )

@router.callback_query(F.data == "add_admin")
async def add_admin(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    """Обработчик кнопки добавления админа"""
    user_id = callback.from_user.id
    is_admin = await users_service.is_admin(session, int(user_id))
    
    if not is_admin:
        await callback.answer("У вас нет прав для выполнения этой операции.")
        return
        
    await callback.message.edit_text(
        "Отправьте Telegram username пользователя, которого хотите сделать администратором.\n"
        "Формат: /add_admin @username"
    )
    

@router.message(F.text.startswith("/add_admin"))
async def process_add_admin(message: types.Message, session: AsyncSession):
    """Обработчик команды добавления админа"""
    try:
        # Проверяем права текущего пользователя
        current_user_id = message.from_user.id
        is_admin = await users_service.is_admin(session, int(current_user_id))
        if not is_admin:
            await message.answer("У вас нет прав для выполнения этой операции.")
            return

        # Получаем ID нового админа из сообщения
        new_admin_nick = message.text.split()[1].replace("@", "")
        new_admin_id = await users_service.find_one_or_none(session=session, filters=UserFilter(tg_nick=new_admin_nick))
        
        # Обновляем статус пользователя в базе данных
        await users_service.update_admin_status(session, new_admin_id, True)
        
        await message.answer(
            f"Пользователь @{new_admin_nick} успешно добавлен в администраторы.",
            reply_markup=main_menu_kb()
        )
    except (IndexError, ValueError):
        await message.answer("Неверный формат команды. Используйте: /add_admin 123456789")
    except Exception as e:
        logger.error(f"Error adding admin: {e}")
        await message.answer("Произошла ошибка при добавлении администратора.")

@router.callback_query(F.data == "remove_admin")
async def remove_admin(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    """Обработчик кнопки удаления админа"""
    user_id = callback.from_user.id
    is_admin = await users_service.is_admin(session, int(user_id))
    
    if not is_admin:
        await callback.answer("У вас нет прав для выполнения этой операции.")
        return
        
    await callback.message.edit_text(
        "Отправьте Telegram username пользователя, которого хотите удалить из администраторов.\n"
        "Формат: /remove_admin @username"
    )
    

@router.message(F.text.startswith("/remove_admin"))
async def process_remove_admin(message: types.Message, session: AsyncSession):
    """Обработчик команды удаления админа"""
    try:
        # Проверяем права текущего пользователя
        current_user_id = message.from_user.id
        is_admin = await users_service.is_admin(session, int(current_user_id))
        if not is_admin:
            await message.answer("У вас нет прав для выполнения этой операции.")
            return

        # Получаем ID нового админа из сообщения
        new_admin_nick = message.text.split()[1].replace("@", "")
        new_admin_id = await users_service.find_one_or_none(session=session, filters=UserFilter(tg_nick=new_admin_nick))
        
        # Обновляем статус пользователя в базе данных
        await users_service.update_admin_status(session, new_admin_id, False)
        
        await message.answer(
            f"Пользователь @{new_admin_nick} успешно удален из администраторов.",
            reply_markup=main_menu_kb()
        )
    except (IndexError, ValueError):
        await message.answer("Неверный формат команды. Используйте: /add_admin 123456789")
    except Exception as e:
        logger.error(f"Error adding admin: {e}")
        await message.answer("Произошла ошибка при добавлении администратора.")