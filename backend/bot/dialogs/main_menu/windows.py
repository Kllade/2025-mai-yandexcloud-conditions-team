from aiogram_dialog import Window, StartMode
from aiogram.types import ContentType
from aiogram.filters import StateFilter
from aiogram_dialog.widgets.text import Const, Format
from aiogram.enums import ParseMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Button, Back, SwitchTo, Row, Next

from bot.dialogs.main_menu.states import MainMenu
from bot.handlers.on_click.main_menu import (
    on_start_question, on_often_questions, on_support, 
    on_back_to_main_menu, on_question_submitted, on_view_history,
    on_ask_another_question
)

def start_window():
    return Window(
        Const(text="👋 Добро пожаловать в чат-бот поддержки!\n\n"
                  "Я помогу вам найти ответы на ваши вопросы. Вы можете:\n"
                  "• Задать свой вопрос\n"
                  "• Посмотреть историю ваших вопросов\n"
                  "• Изучить часто задаваемые вопросы\n"
                  "• Обратиться в поддержку для связи с оператором\n\n"
                  "После получения ответа вы можете оценить его качество, "
                  "поставив реакцию 👍 или 👎"),
        Button(Const("Задать вопрос"), id="start_question", on_click=on_start_question),
        Button(Const("История вопросов"), id="view_history", on_click=on_view_history),
        Button(Const("Часто задаваемые вопросы"), id="search_project", on_click=on_often_questions),
        Button(Const("Поддержка"), id="search_project", on_click=on_support),
        state=MainMenu.start,
    )

def main_menu_window():
    return Window(
        Const(text="Главное меню"),
        Button(Const("Задать вопрос"), id="start_question", on_click=on_start_question),
        Button(Const("История вопросов"), id="view_history", on_click=on_view_history),
        Button(Const("Часто задаваемые вопросы"), id="search_project", on_click=on_often_questions),
        Button(Const("Поддержка"), id="search_project", on_click=on_support),
        state=MainMenu.main_menu,
    )

def start_question_window():
    return Window(
        Const(text="Задайте ваш вопрос:"),
        TextInput(id="question_input", on_success=on_question_submitted),
        Cancel(Const("Выйти"), id="back_to_main_menu", on_click=on_back_to_main_menu),
        state=MainMenu.start_question,
    )


def question_history_window():
    return Window(
        Const(text="История ваших вопросов:"),
        Format("{questions}"),
        Back(Const("Назад"), id="back_to_main_menu"),
        state=MainMenu.question_history,
        parse_mode=ParseMode.HTML
    )


