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

logger = logging.getLogger(__name__)

def get_main_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❓ Задать вопрос", callback_data="ask_question")],
        [InlineKeyboardButton(text="📋 История вопросов", callback_data="question_history")]
    ])

async def on_start_question(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    logger.info("switch to start question")
    await dialog_manager.switch_to(MainMenu.start_question)


async def process_text_question(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager):
    """Обработчик успешного получения текста через TextInput в диалоге"""
    value = widget.get_value()  # Получаем текст из виджета
    
    print(f"Получен текст через TextInput: {value}")
    
    # Передаем значение в функцию обработки вопроса
    await process_question(message, dialog_manager, value)


async def process_question(message: Message, dialog_manager: DialogManager, question_text: str):
    """Общая функция обработки вопроса независимо от источника текста"""
    try:
        
        question = await questions_service.add(
            session=dialog_manager.middleware_data["session"],
            values=QuestionCreate(user_id=message.from_user.id, question_text=question_text, message_id=message.message_id)
        )
        
        # Подготавливаем запрос к API YandexGPT
        prompt = {
            "modelUri": f"gpt://{settings.YANDEX_FOLDER_ID}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": "2000"
            },
            "messages": [
                {
                    "role": "system",
                    "text": "Ты ассистент для абитуриаентов, способный ответить на любой вопрос"
                },
                {
                    "role": "user",
                    "text": question_text
                },
            ]
        }

        # Отправляем запрос к API
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {settings.YANDEX_API_KEY}"
        }

        response = requests.post(url, headers=headers, json=prompt)
        
        # Проверяем успешность ответа
        if response.status_code == 200:
            result = response.json().get("result", {}).get("alternatives", [{}])[0].get("message", {}).get("text", "Не удалось получить ответ")
        else:
            result = f"Ошибка при обращении к API: {response.status_code}"

        # Отправляем ответ пользователю
        await message.answer(
            result,
            allowed_reactions=[
                ReactionTypeEmoji(emoji="👍"),
                ReactionTypeEmoji(emoji="👎")
            ]
        )
        
        try:
            await dialog_manager.switch_to(MainMenu.main_menu)
        except NoContextError as e:
            pass

        
    except Exception as e:
        logger.error(f"Ошибка при обработке вопроса: {e}")
        await message.answer("Произошла ошибка при обработке вашего вопроса. Пожалуйста, попробуйте еще раз.")

        try:
            await dialog_manager.switch_to(MainMenu.main_menu)
        except NoContextError as e:
            pass

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

async def on_ask_another_question(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainMenu.start_question)

async def on_back_to_main_menu(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainMenu.main_menu)

async def on_view_history(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainMenu.question_history)

async def on_often_questions(callback: CallbackQuery, dialog_manager: DialogManager):
    # TODO: Implement FAQ functionality
    pass

async def on_support(callback: CallbackQuery, dialog_manager: DialogManager):
    # TODO: Implement support functionality
    pass

