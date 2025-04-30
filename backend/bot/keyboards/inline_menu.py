from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.core.loader import bot, dp, redis_client
from bot.dialogs.main_menu.states import MainMenu

# --- Клавиатуры ---
def main_menu_kb() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="❓ Задать вопрос", callback_data="ask_question")
    kb.button(text="📜 История вопросов", callback_data="view_history")
    kb.button(text="🔍 Часто задаваемые", callback_data="faq")
    kb.button(text="🛠 Поддержка", callback_data="support")
    return kb.adjust(1, 1, 1, 1).as_markup()

def support_kb() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="❌ Выйти из чата", callback_data="close_support")
    return kb.as_markup()

def close() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="❌ Выйти", callback_data="close")
    return kb.as_markup()

