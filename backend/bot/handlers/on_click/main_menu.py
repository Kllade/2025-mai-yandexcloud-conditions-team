from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, ReactionTypeEmoji
from aiogram_dialog import DialogManager
from bot.dialogs.main_menu.states import MainMenu
from api.questions.service import questions_service
from api.ml.service import ml_service
from api.users.service import users_service
import requests 
from bot.core.config import settings

def get_main_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❓ Задать вопрос", callback_data="ask_question")],
        [InlineKeyboardButton(text="📋 История вопросов", callback_data="question_history")]
    ])

async def on_start_question(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainMenu.start_question)

async def on_question_submitted(message: Message, dialog_manager: DialogManager):
  
    question = await questions_service.add_question(
        user_id=message.from_user.id,
        question_text=message.text,
        message_id=message.message_id
    )

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
            "text": "Ты ассистент дроид, способный помочь в галактических приключениях."
        },
        {
            "role": "user",
            "text": "Привет, Дроид! Мне нужна твоя помощь, чтобы узнать больше о Силе. Как я могу научиться ее использовать?"
        },
        {
            "role": "assistant",
            "text": "Привет! Чтобы овладеть Силой, тебе нужно понять ее природу. Сила находится вокруг нас и соединяет всю галактику. Начнем с основ медитации."
        },
        {
            "role": "user",
            "text": "Хорошо, а как насчет строения светового меча? Это важная часть тренировки джедая. Как мне создать его?"
        }
    ]
}


    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {settings.YANDEX_API_KEY}"
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.text
    await message.answer(
        answer,
        allowed_reactions=[
            ReactionTypeEmoji(emoji="👍"),
            ReactionTypeEmoji(emoji="👎")
        ]
    )

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

async def on_back_to_main_menu(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainMenu.main_menu)

async def on_view_history(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainMenu.question_history)

async def on_often_questions(callback: CallbackQuery, dialog_manager: DialogManager):
    # TODO: Implement FAQ functionality
    pass

async def on_support(callback: CallbackQuery, dialog_manager: DialogManager):
    # TODO: Implement support functionality
    pass

