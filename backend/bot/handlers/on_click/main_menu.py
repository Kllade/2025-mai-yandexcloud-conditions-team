from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, ReactionTypeEmoji
from aiogram_dialog import DialogManager
from aiogram_dialog.api.exceptions import NoContextError
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from bot.dialogs.main_menu.states import MainMenu
from api.questions.service import questions_service
from api.questions.schemas import QuestionCreate
from api.ml.service import ml_service
from api.users.service import users_service
import requests 
from bot.core.config import settings
import logging
from api.cache.redis import redis_client, set_redis_value
from bot.core.loader import bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from bot.keyboards.inline_menu import main_menu_kb, close
from sqlalchemy.ext.asyncio import AsyncSession
logger = logging.getLogger(__name__)


async def process_question(message: Message, state: FSMContext, question_text: str, session: AsyncSession):
    """Общая функция обработки вопроса независимо от источника текста"""
    try:
        
        question = await questions_service.add(
            session=session,
            values=QuestionCreate(user_id=message.from_user.id, question_text=" ".join(question_text.lower().split(" ")), message_id=message.message_id)
        )
        
        
        answer = await ml_service.get_answer(question_text) 
        logger.info(f"answer: {answer}")
        if answer:
            await message.answer(
                answer,
                allowed_reactions=[
                    ReactionTypeEmoji(emoji="👍"),
                    ReactionTypeEmoji(emoji="👎")
                ]
            )
        else:
            await message.answer("Произошла ошибка при получении ответа. Попробуйте позже.")
            
        await state.set_state(MainMenu.start_question)
        await message.answer("✍️ Напишите ваш новый вопрос:", reply_markup=close())

        
    except Exception as e:
        logger.error(f"Ошибка при обработке вопроса: {e}")
        await message.answer("Произошла ошибка при обработке вашего вопроса. Пожалуйста, попробуйте еще раз.")



async def on_reaction_added(message: Message, reaction: str):
    """Обработка добавления реакции"""
    is_helpful = reaction == "👍"
    await users_service.update_reaction_stats(
        user_id=message.from_user.id,
        is_helpful=is_helpful
    )

async def on_reaction_removed(message: Message, reaction: str):
    """Обработка удаления реакции"""
    is_helpful = reaction == "👍"
    await users_service.update_reaction_stats(
        user_id=message.from_user.id,
        is_helpful=not is_helpful, 
        remove=True  
    )


async def on_support(user_id: int, message: Message):
    user_key = f"support:user:{user_id}"
    admin_ids = settings.ADMIN_IDS.split(",")
    logger.info(f"admin_ids: {admin_ids}")
    logger.info(f"user_id: {user_id}")
    if await redis_client.exists(user_key):
        await message.answer("У вас уже открыт чат поддержки. Ожидайте оператора.")
        return
    if str(user_id) in admin_ids:
        await message.answer("Вы являетесь администратором.")
        return
    await set_redis_value(user_key, "waiting")
    await message.answer("Запрос в службу поддержки отправлен. Ожидайте оператора.")

    kb = InlineKeyboardBuilder()
    kb.button(text="Взять чат", callback_data=f"take_{user_id}")
    markup = kb.as_markup()
    for admin_id in settings.ADMIN_IDS.split(","):
        await bot.send_message(
            int(admin_id),
            f"Пользователь <a href=\"tg://user?id={user_id}\">{message.from_user.full_name}</a> запрашивает поддержку.",
            reply_markup=markup,
            parse_mode="HTML"
        )

